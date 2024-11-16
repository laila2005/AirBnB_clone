#!/usr/bin/python3
""" Module of Unittests """
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
import os
import json


class FileStorageTests(unittest.TestCase):
    """ Suite of File Storage Tests """

    my_model = BaseModel()

    def testClassInstance(self):
        """ Check instance """
        self.assertIsInstance(storage, FileStorage)

    def testStoreBaseModel(self):
        """ Test save and reload functions """
        self.my_model.full_name = "BaseModel Instance"
        self.my_model.save()
        storage.reload()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()
        key = bm_dict['__class__'] + "." + bm_dict['id']
        self.assertIn(key, all_objs)

    def testStoreBaseModel2(self):
        """ Test save and reload functions """
        self.my_model.my_name = "First name"
        self.my_model.save()
        storage.reload()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()

        key = bm_dict['__class__'] + "." + bm_dict['id']
        self.assertIn(key, all_objs)
        self.assertEqual(bm_dict['my_name'], "First name")

        create1 = bm_dict['created_at']
        update1 = bm_dict['updated_at']

        self.my_model.my_name = "Second name"
        self.my_model.save()
        storage.reload()
        bm_dict = self.my_model.to_dict()
        all_objs = storage.all()

        self.assertIn(key, all_objs)
        create2 = bm_dict['created_at']
        update2 = bm_dict['updated_at']

        self.assertEqual(create1, create2)
        self.assertNotEqual(update1, update2)
        self.assertEqual(bm_dict['my_name'], "Second name")

    def testHasAttributes(self):
        """ Verify if attributes exist """
        self.assertTrue(hasattr(FileStorage, '_FileStorage__file_path'))
        self.assertTrue(hasattr(FileStorage, '_FileStorage__objects'))

    def testsave(self):
        """ Verify if JSON exists """
        self.my_model.save()
        self.assertTrue(os.path.exists(storage._FileStorage__file_path))
        self.assertEqual(storage.all(), storage._FileStorage__objects)

    def testreload(self):
        """ Test if reload works correctly """
        self.my_model.save()
        dobj = storage.all().copy()
        FileStorage._FileStorage__objects = {}
        self.assertNotEqual(dobj, FileStorage._FileStorage__objects)

        storage.reload()
        self.assertEqual(len(dobj), len(storage.all()))
        for key, value in dobj.items():
            self.assertEqual(value.to_dict(), storage.all()[key].to_dict())

    def testSaveSelf(self):
        """ Check save self """
        msg = "save() takes 1 positional argument but 2 were given"
        with self.assertRaises(TypeError) as e:
            FileStorage.save(self, 100)

        self.assertEqual(str(e.exception), msg)


if __name__ == '__main__':
    unittest.main()
