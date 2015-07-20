import unittest
import main
import json

class TestMain(unittest.TestCase):

    def test_parse(self):
        
        first  = "Booker T., Washington, 87360, 373 781 7380, yellow"
        second = "James Murphy, yellow, 83880, 018 154 6474"
        blank  = ""

        expected_first     = dict([('color', "yellow"), ('firstname', "Booker T."), ('lastname', "Washington"), 
                ('phonenumber', "373-781-7380"), ('zipcode', "87360")])

        expected_second = dict([('color', "yellow"), ('firstname', "James"), ('lastname', "Murphy"), 
                ('phonenumber', "018-154-6474"), ('zipcode', "83880")])
        
        expected_third = 1
    
        self.assertEqual(main.parse(first, 0), expected_first)
        self.assertEqual(main.parse(second, 0), expected_second)
        self.assertEqual(main.parse(blank, 1), expected_third)
    
    def test_process_data(self):
        infile = "test.in"
        outfile = "test.out"
        data = {
                "entries": [
                    {
                        "color": "yellow", 
                        "firstname": "James", 
                        "lastname": "Murphy", 
                        "phonenumber": "018-154-6474", 
                        "zipcode": "83880"
                    },
                    {
                        "color": "yellow", 
                        "firstname": "Booker T.", 
                        "lastname": "Washington", 
                        "phonenumber": "373-781-7380", 
                        "zipcode": "87360"
                    }
                    
                  ], 
                "errors": [
                    1, 
                    3
                ]
            }

        
        expected = json.dumps(data, sort_keys=True, indent=2)
        main.process_data(infile,outfile)
        f = open(outfile, "r").read()
        self.assertEqual(expected,f)


if __name__ == '__main__':
    unittest.main()