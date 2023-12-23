import os

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.env import VirtualBuildEnv
from conan.tools.files import export_conandata_patches, apply_conandata_patches, copy, get, rm, rmdir, replace_in_file
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps, PkgConfigDeps
from conan.tools.layout import basic_layout
from conan.tools.microsoft import unix_path, is_msvc
from conan.tools.scm import Version

required_conan_version = ">=1.54.0"


class LibPlistConan(ConanFile):
    name = "libplist"
    description = "A library to handle Apple Property List format in binary or XML."
    homepage = "https://github.com/libimobiledevice/libplist"
    url = "https://github.com/conan-io/conan-center-index"
    topics = ("libplist", "plist", "libimobiledevice")
    license = ["GPL-2.0", "LGPL-2.1"]

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_cxx": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "enable_cxx": True,
    }

    @property
    def _settings_build(self):
        return getattr(self, "settings_build", self.settings)

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")
        if not self.options.enable_cxx:
            self.settings.rm_safe("compiler.libcxx")
            self.settings.rm_safe("compiler.cppstd")

    def layout(self):
        basic_layout(self, src_folder="src")

    def requirements(self):
        pass

    def build_requirements(self):
        self.tool_requires("automake/1.16.5")
        self.tool_requires("autoconf/2.71")
        self.tool_requires("libtool/2.4.7")
        self.tool_requires("m4/1.4.19")
        if self._settings_build.os == "Windows":
            self.win_bash = True
            if not self.conf.get("tools.microsoft.bash:path", check_type=str):
                self.tool_requires("msys2/cci.latest")

    def validate(self):
        pass
        # # Note that elfutils cannot be built on macOS
        # # Example Error: "configure: error: __thread support required"
        # # Reference: https://stackoverflow.com/questions/72372589/elfutils-build-error-on-mac-configure-error-thread-support-required
        # if self.settings.os == "Macos":
        #     raise ConanInvalidConfiguration("elfutils does not support macOS.")
        #
        # if Version(self.version) >= "0.186":
        #     if self.settings.compiler == "apple-clang" or is_msvc(self):
        #         raise ConanInvalidConfiguration(f"Your compiler {self.settings.compiler} is not supported. "
        #                                         "elfutils only supports GCC and Clang.")
        # else:
        #     if self.settings.compiler in ("clang", "apple-clang") or is_msvc(self):
        #         raise ConanInvalidConfiguration(f"Your compiler {self.settings.compiler} is not supported. "
        #                                         "elfutils only supports GCC.")
        # if self.settings.compiler != "gcc":
        #     self.output.warning(f"Your compiler {self.settings.compiler} is not GCC.")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        env = VirtualBuildEnv(self)
        env.generate()
        tc = AutotoolsToolchain(self)
        tc.configure_args.append("--without-cython")
        tc.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        self._patch_sources()
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        copy(self, pattern="COPYING*", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        autotools = Autotools(self)
        autotools.install()
        rmdir(self, os.path.join(self.package_folder, "share"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "libplist")
        self.cpp_info.set_property("cmake_target_name", "libplist::libplist")
        self.cpp_info.libs = ["plist-2.0"]
        if self.options.enable_cxx:
            self.cpp_info.libs.append("plist++-2.0")
