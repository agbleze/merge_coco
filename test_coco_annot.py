
#%%

import json
import os
import pytest

#%%

os.getcwd()


#%%


@pytest.fixture()
def coco_data(coco_annotation_file):
    with open(coco_annotation_file, "r") as f:
        coco_data = json.load(f)
    return coco_data
    

def test_category_names_are_unique(coco_data):
        
    unique_cat_names = {cat["name"] for cat in coco_data["name"]}
    
    actual_cat_names = [cat["name"] for cat in coco_data["name"]]
    
    assert len(unique_cat_names) == len(actual_cat_names)
    
    
def test_image_names_are_unique(coco_data):
    unique_image_names = {img["file_name"] for img in coco_data["images"]}
    actual_image_names = [img["file_name"] for img in coco_data["images"]]
    assert len(unique_image_names) == len(actual_image_names)
    
def test_annotations_bbox_contains_zero_values(coco_data):
    #bboxes = []
    bboxes = [annot["bbox"] for annot in coco_data["annotations"]]   
    
#%%

bb = [[0, 0.0, 0.00000000], [0, 9, 0.0, 0]]

for b in bb:
    print(all(b) == 0)    
        

#%%
all([0, 9, 0.0, 0]) == 0  



# %%
import unittest
import json

def load_coco_annotations(file_path):
    """
    Loads COCO annotations from a JSON file.

    Args:
        file_path (str): Path to the COCO annotation file.

    Returns:
        dict: Parsed COCO annotation data.
    """
    with open(file_path, 'r') as f:
        coco_data = json.load(f)
    return coco_data

def check_zero_bboxes(coco_data):
    """
    Checks if any bounding box (bbox) in COCO annotations has only zero values.

    Args:
        coco_data (dict): COCO annotation data.

    Returns:
        bool: True if any bbox has only zero values, False otherwise.
    """
    for annotation in coco_data['annotations']:
        bbox = annotation['bbox']
        if all(value == 0 for value in bbox):
            return True
    return False

class TestZeroBboxes(unittest.TestCase):
    def test_zero_bboxes(self):
        # Create a mock COCO annotation data with zero bboxes
        mock_coco_data = {
            "annotations": [
                {"bbox": [0, 0, 0, 0]},
                {"bbox": [1, 0, 0, 0]},
                {"bbox": [0, 0, 0, 1]},
            ]
        }

        # Check if the function correctly identifies zero bboxes
        self.assertTrue(check_zero_bboxes(mock_coco_data))

        # Create a mock COCO annotation data without zero bboxes
        mock_coco_data_no_zero = {
            "annotations": [
                {"bbox": [1, 2, 3, 4]},
                {"bbox": [0, 1, 2, 3]},
                {"bbox": [2, 2, 2, 2]},
            ]
        }

        # Check if the function correctly identifies no zero bboxes
        self.assertFalse(check_zero_bboxes(mock_coco_data_no_zero))

if __name__ == "__main__":
    unittest.main()
