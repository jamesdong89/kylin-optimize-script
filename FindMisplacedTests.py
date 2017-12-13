from lxml import html
import os, fnmatch
import sys

dir = sys.argv[1]
project = sys.argv[2]
print dir
print project
# dir = "/Users/matthewd/projects/kylin-master"
test_map = dict()

def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def test_target_module(file_abs_path):
    file_path_list = file_abs_path.split("/")
    file_last_ele = file_path_list[len(file_path_list) - 1]
    test = ""
    file_split = file_last_ele.split("_")

    if "_" in file_last_ele and ".html" in file_last_ele:
        test = file_split[0] + ".java"

    if test != "":
        tree = html.parse(file_abs_path)
        test_and_method = file_split[0] + "_" + file_split[1]

        spans = tree.xpath('//span[@class="sortValue"]/text()')
        target_classes = []
        for i in spans:
            if not i.replace('.', '1').isdigit():
                target_classes.append(i)

        test_files = find_all(test, dir)
        test_module = ""
        for file_path in test_files:
            if "/src/test/java" in file_path:
                # print file_path
                test_module = file_path[len(dir):file_path.find("/src/test/java")]
# for core cube package test only
#         if test_module == "core-cube":

        class_modules = []
        test_name = test_and_method.split("_")[0]


        for cls in target_classes:
                cls_list = cls.split(".")
                last_ele = cls_list[-1]
                class_paths = find_all(last_ele + ".java", dir)
                if len(class_paths) == 0:
                    last_ele = cls_list[-2]
                    class_paths = find_all(last_ele + ".java", dir)

                for path in class_paths:
                    prefix = "/src/main/java"
                    for i in xrange(len(cls_list) - 1):
                        prefix += "/" + cls_list[i]

                    if prefix in path:
                        class_module = path[len(dir):path.find("/src/main/java")]
                        if test_name in test_map:
                            class_modules = test_map[test_name]
                            if class_module not in class_modules:
                                class_modules.append(class_module)
                        else:
                            class_modules = []
                            class_modules.append(class_module)
                            test_map[test_name] = class_modules


        test_map[test_and_method] = (test_module, class_modules)
        print "test and method: " + test_and_method
        print "test module: " + test_module
        print "class modules:"
        print class_modules



for root, dirs, files in os.walk(dir + "/target/site/clover/org/apache/" + project):
    for file in files:
        test_target_module(root + "/" + file)

# for k in test_map:
#     print "test:" + k
#     print "class module"
#     print test_map[k]





