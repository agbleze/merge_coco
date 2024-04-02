
#%%
import json
import copy

def merge_coco_annotations(annotation_files):
    # Initialize merged COCO dictionary
    merged_coco = {
        "info": {},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    # Initialize category ID mapping
    category_id_mapping = {}
    
    image_id_record = []
    annotation_id_record = []

    # Initialize annotation ID counter
    annotation_id_counter = 1

    for file_path in annotation_files:
        with open(file_path, "r") as f:
            coco_data = json.load(f)

            # Merge categories
            for category in coco_data["categories"]:
                if category["id"] not in category_id_mapping:
                    category_id_mapping[category["id"]] = len(merged_coco["categories"]) + 1
                    merged_coco["categories"].append(category)

            # Merge images
            for image in coco_data["images"]:
                image_id = image["id"]
                filename = image["file_name"]
                print(f"filename: {filename}")
                
                if image_id not in image_id_record:
                    print(f"image_id: {image_id} not found in existing annotations hence used for merging")
                    merged_coco["images"].append(image)
                    image_id_record.append(image_id)
                    
                    annot_for_img_id = [annot for annot in coco_data["annotations"] 
                                        if image_id==annot["image_id"]
                                        ]
                    for ann in annot_for_img_id:                      
                        if ann["id"] not in annotation_id_record:
                            merged_coco["annotations"].append(ann)
                            annotation_id_record.append(ann["id"])
                            print(f"annotation id: {ann['id']} not already existing hence used for merging")
                        else:
                            ann_increase = max(annotation_id_record) + 1
                            print(f"annotation id: {ann['id']} already exist hence increased to {ann_increase} for merging")
                            ann["id"] = ann_increase
                            merged_coco["annotations"].append(ann)
                            annotation_id_record.append(ann_increase)
                    
                    # for annot in coco_data["annotations"]:
                    #     _image_id = annot["image_id"]
                        
                    #     if _image_id == image_id:
                    #         merged_coco["annotations"].append(annot)
                            #annotation_id_record.append(annot["id"])
                            
                else: 
                    annot_for_img_id = [annot for annot in copy.deepcopy(coco_data["annotations"]) 
                                         if int(image_id)==int(annot["image_id"])
                                        ]
                    
                    #print(f"num_annotations: {len(annot_for_img_id)}\n")
                    #print(f"annotations \n {annot_for_img_id}\n")
                    image_id_inc = max(image_id_record) + 1
                    #print(f"image_id: {image_id} already exists in annotations hence increased to {image_id_inc} for uniqueness")
                    image["id"] = image_id_inc
                    merged_coco["images"].append(image)
                    image_id_record.append(image_id_inc)
                    
                    #updated_annot = []
                    # no = 0
                    # for annot in  coco_data["annotations"]:
                    #     if annot["image_id"] == image_id:
                    #         annot["image_id"] = image_id_inc
                    #         no += 1
                    # print(f"num of annot updated: {no}")
                        #updated_annot.append(annot)
                    
                    # annot_for_img_id = [annot for annot in coco_data["annotations"] 
                    #                     if image_id==annot["image_id"]
                    #                     ]
                    #qno = 0
                    update_list = []
                    for ann in annot_for_img_id: 
                        if ann["image_id"] not in image_id_record:
                            print(f"HERE -- {ann['image_id']}")
                            pass
                        else:
                            #print(f"image_id_record: {image_id_record} \n")
                            #image_id_inc = max(image_id_record) + 1
                            ann["image_id"] = image_id_inc
                            
                        if ann["id"] not in annotation_id_record:
                            print(f"ann HERE --{ann['id']}")
                            pass
                        else:
                            #print(f"annotation_id_record: {annotation_id_record}\n")
                            new_annot = max(annotation_id_record) + 1
                            ann["id"] = new_annot
                            annotation_id_record.append(new_annot)
                        update_list.append(ann)
                    print(f"update_list: {update_list} \n")
                    merged_coco["annotations"].extend(update_list)
                    
                        
                        
                        #if ann["image_id"] == image_id:
                        # if ann["image_id"] == image_id:                    
                        #     if ann["id"] not in annotation_id_record:
                        #         merged_coco["annotations"].append(ann)
                        #         annotation_id_record.append(ann["id"])
                                #print(f"annotation id: {ann['id']} not already existing hence used for merging")
                            #else: # check logic here
                                #ann_increase = max(annotation_id_record) + 1
                                #print(f"annotation id: {ann['id']} already exist hence increased to {ann_increase} for merging")
                                # ann["id"] = ann_increase
                                # merged_coco["annotations"].append(ann)
                                # annotation_id_record.append(ann_increase)
                    #print(f"num of qualified annot: {qno}")
                            
                    # for annot in coco_data["annotations"]:
                    #     annt_image_id = annot["image_id"]
                        
                    #     if annt_image_id == image_id:
                    #         annot["image_id"] = image_id_inc
                    #         merged_coco["annotations"].append(annot)
     
                
                ## custom
                # take 
                # check id in image

            # Merge annotations
            # for annotation in coco_data["annotations"]:
            #     annotation["id"] = annotation_id_counter
            #     annotation_id_counter += 1
            #     annotation["category_id"] = category_id_mapping[annotation["category_id"]]
            #     merged_coco["annotations"].append(annotation)

    return merged_coco

#%% Example usage

test_coco_file = "/home/lin/codebase/merge_coco/test_annotations.json"
valid_coco_file = "/home/lin/codebase/merge_coco/valid_annotations.json"
annotation_files = [test_coco_file, valid_coco_file]
merged_coco_data = merge_coco_annotations(annotation_files)

#%% Save merged COCO data to a new file
with open("cor4_merged_annotations.json", "w") as outfile:
    json.dump(merged_coco_data, outfile, indent=4)

print("Merged COCO annotations saved to merged_annotations.json")


#%%
with open(valid_coco_file, "r") as f:
    coco_data = json.load(f)

#%%
#sel_dict = {}

for img in coco_data["images"]:
    if img["id"] == 210:
        sel_dict = [anno for anno in coco_data["annotations"] if anno["image_id"] == img["id"]]
        
       # img_id_new = max(sel_dic)
        annot_li = [765, 766, 767, 768]
        imgid_list = [210]
        update_list = []
        for el in sel_dict:
            if el["image_id"] not in imgid_list:
                pass
            else:
                imgidinc = max(imgid_list) + 1
                el["image_id"] = imgidinc
            if el["id"] not in annot_li:
                pass
            else:
                new_annot = max(annot_li) + 1
                el["id"] = new_annot
                annot_li.append(new_annot)
            update_list.append(el)
            


#%%

len(sel_dict)        

#%%
eg_img_idrec = [1,2,3]

len(eg_img_idrec)


#%%
## TO DO 


#%%

dict_inc = {"id": 10}
dc_list = [12, 10, 1, 2, 3]
#%%
dict_inc["id"] = max(dc_list) + 1


#%%##
la = [1,2,3,4]
lb = [5,6,7]
la.extend(lb)
print(la)
#eg_img_idrec
# %%
## fields to update
# annotations --> image_id
# images --> id

## also make sure id in categories is unique and not duplicated 
## 

#%%
egx = [{'id': 739, 'image_id': 210, 'category_id': 9, 'bbox': [21, 114, 489.5, 401.5], 'area': 196534.25, 'segmentation': [], 'iscrowd': 0}, {'id': 740, 'image_id': 210, 'category_id': 9, 'bbox': [102, 0, 195, 250], 'area': 48750, 'segmentation': [], 'iscrowd': 0}, {'id': 765, 'image_id': 210, 'category_id': 12, 'bbox': [377, 103, 152, 215], 'area': 32680, 'segmentation': [], 'iscrowd': 0}, {'id': 766, 'image_id': 210, 'category_id': 12, 'bbox': [1, 323, 109, 96], 'area': 10464, 'segmentation': [], 'iscrowd': 0}, {'id': 767, 'image_id': 210, 'category_id': 12, 'bbox': [122, 468, 152, 147], 'area': 22344, 'segmentation': [], 'iscrowd': 0}, {'id': 768, 'image_id': 210, 'category_id': 12, 'bbox': [54, 181, 83, 84], 'area': 6972, 'segmentation': [], 'iscrowd': 0}]

