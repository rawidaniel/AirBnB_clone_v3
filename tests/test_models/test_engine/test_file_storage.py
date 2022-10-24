@unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.class.name + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test that get properly get objects from specified Id and class"""
        new_obj = State(name='phenselivia')
        storage = FileStorage()
        obj = storage.get(State, 'fake id')
        self.assertIsNone(obj)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test that count properly count objects"""
        storage = FileStorage()
        storage.reload()
        all_count = storage.count()
        clss_count = storage.count("State")
        self.assertIsInstance(all_count, int)
        self.assertIsInstance(all_count, int)
        self.assertGreaterEqual(all_count, clss_count)
