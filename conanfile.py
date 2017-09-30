from conans import ConanFile, CMake

class MitkConan(ConanFile):
    name = "MITK"
    version = "2016.11"
    url = "https://github.com/cinderblocks/conan-mitk"
    license = "http://mitk.org/wiki/License"
    description = "The Medical Imaging Interaction Toolkit (MITK) is a free open-source software system for development of interactive medical image processing software."
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "acvd": [True, False],
        "qt": [True, False],
        "system_qt": [True, False],
        "blueberry": [True, False],
        "boost": [True, False],
        "build_boost": [True, False],
        "opencv": [True, False],
        "python": [True, False]}
    default_options = "=False\n".join(options.keys()) + "=False"
    generators = "cmake"

    def requirements(self):
        if self.options.qt == True and not self.options.system_qt:
            self.requires("Qt/5.9.1@slidewave/stable")
        if self.options.boost and not self.options.build_boost:
            self.requires("Boost/1.64.0@slidewave/stable")


    def source(self):
        self.run("git clone https://phabricator.mitk.org/source/mitk.git MITK")
        self.run("cd MITK && git checkout tags/v2016.11")

    def build(self):
        cmake = CMake(self)
        if self.options.system_qt:
            cmake.definitions["CMAKE_PREFIX_PATH"] = "F:/Developer/Qt/5.9.1/msvc2017_64"
        elif self.options.qt:
            cmake.definitions["CMAKE_PREFIX_PATH"] = self.deps_cpp_info["Qt"].rootpath[0]
        if self.options.acvd:
            cmake.definitions["MITK_USE_ACVD"] = True
        if self.options.blueberry:
            cmake.definitions["MITK_USE_BLUEBERRY"] = True
        if self.options.boost:
            cmake.definitions["MITK_USE_Boost"] = True
            if not self.options.build_boost:
                boost_info = self.deps_cpp_info["Boost"]
                cmake.definitions["MITK_USE_Boost_LIBRARIES"] = boost_info.lib_paths[0]
                cmake.definitions["EXTERNAL_BOOST_ROOT"] = boost_info.lib_paths[0] + "/../"
        if self.options.opencv:
            cmake.definitions["MITK_USE_OpenCV"] = True
        if self.options.python:
            cmake.definitions["MITK_USE_Python"] = True

        #self.run("mkdir MITK-superbuild")
        cmake.configure(source_dir="MITK")
        cmake.build(target="install")

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="lib", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)

    def package_info(self):
        return super(MitkConan, self).package_info()
