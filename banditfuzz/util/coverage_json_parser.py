import json
from .parser import args as settings
import os

class jsonParser:
    def __init__(self, json_file="coverage.json"):
        self.json_file = json_file
        self.getBaseJsonMap()
        self.baseLineCoverage = self.getBaseLineCoverage()
        self.json_map = []


    def getBaseJsonMap(self):
        for solver in settings.target_solvers:
            cmd = f"gcovr -r {solver} --json -o util/{self.json_file}"
            os.system(cmd)
            with open(self.json_file) as file:
                self.json_map.append(json.load(file))
            file.close()

    def getNewJsonMap(self):
        self.new_json_map = []
        for solver in settings.target_solvers:
            cmd = f"gcovr -r {solver} --json -o util/{self.json_file}"
            os.system(cmd)
            with open(self.json_file) as file:
                self.new_json_map.append(json.load(file))
                file.close()

    def getBaseLineCoverage(self):
        self.coverageData = []

        ''' for a in range(len(self.json_map["files"])):
            for b in range(len(self.json_map["files"][a]["lines"])):
                for c in range(len(self.json_map["files"][a]["lines"][b]["branches"])):
                    if self.json_map["files"][a]["lines"][b]["branches"][c]["count"] > 0:
                        total_branches_visited += 1
                        self.json_map["files"][a]["lines"][b]["branches"][c]["visited"] = True
                    else:
                        self.json_map["files"][a]["lines"][b]["branches"][c]["visited"] = False
                    total_branch_count += 1'''

        for i in range(len(settings.target_solvers)):
            total_branches_visited = 0
            total_branch_count = 0
            for file in self.json_map[i]["files"]:
                for line in file["lines"]:
                    for branch in line["branches"]:
                        if branch["count"] > 0:
                            total_branches_visited += 1
                        total_branch_count += 1
            self.coverageData.append((i, float(total_branches_visited)/float(total_branch_count)*100))


        #return (float(total_branches_visited) / float(total_branch_count)) * 100.0

    def getNewCoverage(self): #might not be necessary
        self.getNewJsonMap()
        increase = False
        for a in range(len(self.new_json_map["files"])):
            for b in range(len(self.new_json_map["files"][a]["lines"])):
                for c in range(len(self.new_json_map["files"][a]["lines"][b]["branches"])):
                    if self.new_json_map["files"][a]["lines"][b]["branches"][c]["count"] > 0 and self.json_map["files"][a]["lines"][b]["branches"][c]["visited"]==False:
                        #self.total_branch_count += 1
                        self.unique_branches += 1
                        self.json_map["files"][a]["lines"][b]["branches"][c]["visited"] = True
                        increase = True
        return increase, (float(self.unique_branches)/float(self.total_branch_count)) * 100



'''branch_coverage = (float(total_branches_visited) / float(total_branch_count)) * 100.0
print("total_branches_visited = %d" % (total_branches_visited))
print("total_branch_count = %d" % (total_branch_count))
print("branch coverage = %f %%" % (branch_coverage))'''

