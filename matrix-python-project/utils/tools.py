import sys, os, time, json
sys.path.append(os.getcwd())


class Tools(object):

    @staticmethod
    def string2timestamp(duration):
        duration_list = duration.split(":")
        if duration_list[0] != "00":
            duration_timestamp = int(duration_list[0]) * 60 + int(duration_list[1])
        else:
            duration_timestamp = int(duration_list[1])

        return duration_timestamp

    @staticmethod
    def assert_file_exist(file_path):
        assert os.path.isfile(file_path)
