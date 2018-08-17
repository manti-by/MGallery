import uuid

from celery import Celery

from core.conf import settings
from core.comparator import Comparator
from core.detector import Detector
from core.utils import (
    extract_gallery_data,
    extract_image_data
)
from service import (
    DescriptorService,
    GalleryService,
    ImageService,
    PersonService
)

app = Celery()
app.conf.broker_url = settings['celery_broker']
app.conf.ONCE = {
  'backend': 'celery_once.backends.Redis',
  'settings': {
      'url': settings['celery_broker'],
      'default_timeout': 60
  }
}


@app.task
def process_gallery(gallery_id):
    service = GalleryService()
    gallery = service.get(id=gallery_id)
    if gallery is not None:
        data = extract_gallery_data(gallery.path)
        service.update(id=gallery.id, **data)
        return 'Successfully processed gallery with id %d' % gallery_id
    return 'Cant find gallery with id %d' % gallery_id


@app.task
def process_image(image_id):
    service = ImageService()
    image = service.get(id=image_id)
    if image is not None:
        data = extract_image_data(image.path)
        dimensions = data.pop('dimensions')
        if dimensions is not None:
            data['width'] = dimensions[0]
            data['height'] = dimensions[1]
            service.update(id=image.id, **data)
        return 'Successfully processed image with id %d' % image_id
    return 'Cant find image with id %d' % image_id


@app.task
def find_faces(image_id):
    descriptors = []
    image = ImageService().get(id=image_id)
    if image is not None:
        detector = Detector(image.path)
        detector.run()
        service = DescriptorService()
        for descriptor in detector.descriptors:
            service.create(image_id=image.id,
                                       vector=list(descriptor))
            descriptors.append(descriptors)
        return 'Successfully found %d faces for image %d' % (len(descriptors), image_id)
    else:
        return 'Cant find image with id %d' % image_id


@app.task
def find_duplicates(image_id):
    duplicates = 0
    service = ImageService()
    image = service.get(id=image_id)
    if image is not None:
        for duplicate in service.list():
            if image.phash == duplicate.phash and image.id != duplicate.id:
                image.similar.append(duplicate)
                duplicates += 1
        service.commit([image])
        return 'Successfully found %d duplicates for image %d' % (duplicates, image_id)
    else:
        return 'Cant find image with id %d' % image_id


@app.task
def compare_faces(descriptor_id):
    ds = DescriptorService()
    descriptor = ds.get(id=descriptor_id)
    if descriptor is not None:
        comparator = Comparator(descriptor)
        person_id = comparator.find_person()
        if person_id is None:
            person_id = PersonService().create(
                name=uuid.uuid4().hex[:8]
            )
        ds.update(
            id=descriptor_id,
            person_id=person_id

        )
        return 'Updated descriptor with person id %d' % person_id
    else:
        return 'Cant find descriptor with id %d' % descriptor_id
