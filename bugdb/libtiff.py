import shutil
from pathlib import Path
from typing import Any, Dict, List

from .bug import Bug
from .build import Build
from .utils import ROOT, sh

LIBTIFF_PATH = ROOT.joinpath("libtiff")


class Libtiff(Build):
    def __init__(self, version: str, simulate: bool = False) -> None:
        url = "https://github.com/vadz/libtiff/archive/{}.tar.gz".format(version)
        super().__init__(url, LIBTIFF_PATH, simulate, enable_address_sanitizer=True)

    def pre_build(self) -> None:
        sh(
            ["sed", "-i", "-e", "s!ACLOCAL_AMFLAGS = -I ./m4!!", "Makefile.am"],
            self.simulate,
            dir=str(self.build_path),
        )


class LibtiffBug(Bug):
    def __init__(self, *args: Any, bug_id: int, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.bug_id = bug_id

    def working_directory(self) -> Path:
        return LIBTIFF_PATH.joinpath("ID-{}".format(self.bug_id))

    def extra_env(self) -> Dict[str, str]:
        env = super().extra_env()
        env.update(dict(LD_LIBRARY_PATH=str(self.libtiff_libs)))
        return env

    def executable(self) -> str:
        exe = self._command[0]
        libtiff = Libtiff(self.version, simulate=self.simulate)
        libtiff.build()
        self.libtiff_libs = libtiff.build_path.joinpath("libtiff", ".libs")
        return str(libtiff.build_path.joinpath("tools", ".libs", exe))


def libtiff_bugs(bug_ids: Dict[int, str]) -> List[Bug]:
    bugs = []  # type: List[Bug]
    commands = {}  # type: Dict[int, List[str]]

    commands[111] = ["tiff2pdf", "testcase.tif", "-o", "@tempdir@/test.pdf"]
    commands[139] = [
        "tiff2pdf",
        "10-10-8-m6-63c8b14ea08a18c884d05a3431716047.tif-crash",
        "-o",
        "@tempdir@/test.pdf",
    ]
    commands[141] = ["tiff2pdf", "wololo.tif", "-o", "@tempdir@/test.pdf"]
    commands[141] = ["tiff2pdf", "wololo.tif", "-o", "@tempdir@/test.pdf"]
    commands[162] = ["tiff2pdf", "testcase.04.tif", "-o", "@tempdir@/test.pdf"]
    commands[163] = ["rgb2ycbcr", "test2.tif", "@tempdir@/test.pdf"]
    commands[180] = ["tiff2rgba", "flower-palette-16.tif", "@tempdir@/test.pdf"]
    commands[212] = ["gif2tiff", "008.gif", "@tempdir@/test.pdf"]
    commands[218] = ["tiffcp", "-c", "none", "testcase.tif", "@tempdir@/0.none.tif"]
    commands[219] = ["tiff2pdf", "05_tiff2pdf.tiff", "-o", "@tempdir@/test.pdf"]
    commands[220] = ["tiffcmp", "10_tiffcmp.tiff", "00_basefile.tiff"]
    commands[221] = ["thumbnail", "02_thumbnail.tiff", "@tempdir@/out.tiff"]
    commands[222] = ["thumbnail", "03_thumbnail.tiff", "@tempdir@/out.tiff"]
    commands[223] = ["thumbnail", "01_thumbnail.tiff", "@tempdir@/out.tiff"]
    commands[223] = ["thumbnail", "01_thumbnail.tiff", "@tempdir@/out.tiff"]
    commands[224] = ["tiff2bw", "04_tiff2bw.tiff", "@tempdir@/out.tiff"]
    commands[228] = ["tiff2pdf", "ycbcr-cat.tif", "-o" "@tempdir@/test.pdf"]
    commands[229] = ["tiff2pdf", "testcase.jpeg.tiff", "-o" "@tempdir@/test.pdf"]
    commands[230] = ["tiff2rgba", "fpe1.tif", "@tempdir@/test.pdf"]
    commands[264] = ["rgb2ycbcr", "broken_2.tif", "@tempdir@/test.pdf"]

    commands[265] = ["tiffinfo", "-d", "libtiff5.tif"]
    commands[269] = ["tiffcrop", "CVE-2016-5321.tif", "@tempdir@/out.tif"]
    commands[270] = ["tiffcrop", "CVE-2016-5323.tif", "@tempdir@/out.tif"]
    commands[273] = ["tiffcrop", "CVE-2016-3991.tif", "@tempdir@/out.tif"]
    commands[274] = [
        "rgb2ycbcr",
        "-c",
        "zip",
        "-r",
        "0",
        "-h",
        "0",
        "-v",
        "2",
        "CVE-2016-3624.tif",
        "@tempdir@/out.tif",
    ]
    commands[281] = ["tiffinfo", "-d", "ShowTile_heap-oob.tif"]

    class TiffsetBug(LibtiffBug):
        def pre_hook(self) -> None:
            tif = LIBTIFF_PATH.joinpath("ID-282", "19_tiffset.tiff")
            shutil.copyfile(str(tif), str(Path(self.directory.name).joinpath("19_tiffset.tiff")))

    bugs.append(
        TiffsetBug(
            "libtiff-282",
            bug_id=282,
            version=bug_ids[282],
            command=["tiffset", "@tempdir@/19_tiffset.tiff"],
        )
    )

    commands[286] = ["tiffset", "test049"]
    commands[287] = ["tiffcrop", "2016-11-10-heap-buffer-overflow.tif", "@tempdir@/out"]

    commands[291] = ["tiff2pdf", "testcase", "-o", "@tempdir@/test.pdf"]

    commands[292] = ["tiff2pdf", "testcase", "-o", "@tempdir@/test.pdf"]

    commands[293] = [
        "tiff2bw",
        "2016-11-16-tiff2bw-invalid-read.tif",
        "@tempdir@/test.pdf",
    ]

    commands[295] = ["tiffcp", "testcase", "@tempdir@/out"]

    commands[297] = [
        "tiffcp",
        "00071-libtiff-heapoverflow-_TIFFmemcpy",
        "@tempdir@/out",
    ]

    commands[298] = [
        "tiffcp",
        "-i",
        "00074-libtiff-heapoverflow-TIFFFillStrip",
        "@tempdir@/out",
    ]

    commands[299] = ["tiffmedian", "00083-libtiff-fpe-OJPEGDecodeRaw", "@tempdir@/out"]

    commands[300] = [
        "tiffcrop",
        "-i",
        "00100-libtiff-heapoverflow-_TIFFFax3fillruns",
        "@tempdir@/out",
    ]

    commands[301] = [
        "tiffcrop",
        "-i",
        "00101-libtiff-heapoverflow-combineSeparateSamples16bits",
        "@tempdir@/out",
    ]

    commands[303] = ["tiffinfo", "-Dijr", "00056-libtiff-nullptr-TIFFReadRawData"]

    commands[305] = [
        "tiffcp",
        "-i",
        "00067-libtiff-heapoverflow-tiffcp",
        "@tempdir@/out",
    ]

    commands[308] = [
        "tiffcp",
        "-i",
        "00072-libtiff-assert-readSeparateTilesIntoBuffer",
        "@tempdir@/out",
    ]

    commands[309] = ["tiff2ps", "00108-libtiff-heapoverflow-PSDataBW", "@tempdir@/out"]

    commands[310] = [
        "tiff2ps",
        "00107-libtiff-heapoverflow-PSDataColorContig",
        "@tempdir@/out",
    ]

    commands[311] = ["tiff2pdf", "-j", "testcase", "-o", "@tempdir@/out"]

    commands[312] = ["tiff2rgba", "ycbcr_14_lzw.tif", "@tempdir@/out"]

    commands[313] = [
        "tiff2pdf",
        "00110-libtiff-memcpy-param-overlap-_TIFFmemcpy",
        "-o",
        "@tempdir@/out",
    ]

    # bug_ids[314] = "ad2fccb"

    commands[314] = [
        "tiff2pdf",
        "00111-libtiff-invalidread-t2p_writeproc",
        "-o",
        "@tempdir@/out",
    ]

    commands[315] = [
        "tiff2pdf",
        "00112-libtiff-heapoverflow-_TIFFmemcpy",
        "-o",
        "@tempdir@/out",
    ]

    for bug_id, command in commands.items():
        bugs.append(
            LibtiffBug(
                "libtiff-{}".format(bug_id),
                bug_id=bug_id,
                version=bug_ids[bug_id],
                command=command,
            )
        )
    return bugs


## 111
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/testcase.tiff' -o 'PATH_TO_TEST_DIR/test.pdf'

## 139
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/10-10-8-m6-63c8b14ea08a18c884d05a3431716047.tif-crash' -o 'PATH_TO_TEST_DIR/test.pdf'

## 141
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/wololo.tif -o 'PATH_TO_TEST_DIR/test.pdf'

## 149

## 158

## 161
#
# $ ./installer/bin/tiffinfo crash.tif

## 162
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/testcase.04.tif -o 'PATH_TO_TEST_DIR/test.pdf'

## 163
#
# $ ./installer/bin/rgb2ycbcr 'PATH_TO_TEST_DIR/test2.tif 'PATH_TO_TEST_DIR/test.pdf'

## 171

## 172

## 175

## 178

## 180
#
# $ ./installer/bin/tiff2rgba 'PATH_TO_TEST_DIR/flower-palette-16.tif 'PATH_TO_TEST_DIR/test.pdf'

## 181

## 182

## 187

## 188

## 192

## 209

## 212
#
# $ ./installer/bin/gif2tiff 'PATH_TO_TEST_DIR/008.gif' 'PATH_TO_TEST_DIR/out'

## 218
#
# $ ./installer/bin/tiffcp -c none 'PATH_TO_TEST_DIR/testcase.tif' 'PATH_TO_TEST_DIR/0.none.tif'
## 219
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/05_tiff2pdf.tiff' -o 'PATH_TO_TEST_DIR/test.pdf'

## 220
#
# $ ./installer/bin/tiffcmp 'PATH_TO_TEST_DIR/10_tiffcmp.tiff' 'PATH_TO_TEST_DIR/00_basefile.tiff'
## 221
#
# $ ./installer/bin/thumbnail 'PATH_TO_TEST_DIR/02_thumbnail.tiff' 'PATH_TO_TEST_DIR/out.tiff'
#

## 222
#
# $ ./installer/bin/thumbnail 'PATH_TO_TEST_DIR/03_thumbnail.tiff' 'PATH_TO_TEST_DIR/out.tiff'
#

## 223
#
# $ ./installer/bin/thumbnail 'PATH_TO_TEST_DIR/01_thumbnail.tiff' 'PATH_TO_TEST_DIR/out.tiff'
#

## 224
#
# $ ./installer/bin/tiff2bw 'PATH_TO_TEST_DIR/04_tiff2bw.tiff' 'PATH_TO_TEST_DIR/out.tiff'
#

## 228
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/ycbcr-cat.tif' -o 'PATH_TO_TEST_DIR/test.pdf'

## 229
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/testcase.jpeg.tiff' -o 'PATH_TO_TEST_DIR/test.pdf'

## 230
#
# $ ./installer/bin/tiff2rgba 'PATH_TO_TEST_DIR/fpe1tiff' -o 'PATH_TO_TEST_DIR/test.pdf'

## 235
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/testcase.jpeg.tiff' -o 'PATH_TO_TEST_DIR/test.pdf'

## 264
#
# $ ./installer/bin/rgb2ycbcr 'PATH_TO_TEST_DIR/broken_2.tiff' 'PATH_TO_TEST_DIR/test.pdf'

## 265
#
# $ ./installer/bin/tiffinfo -d 'PATH_TO_TEST_DIR/libtiff5.tiff'
## 269
#
# $ ./installer/bin/tiffcrop 'PATH_TO_TEST_DIR/CVE-2016-5321.tif' 'PATH_TO_TEST_DIR/out.tif'
## 270
#
# $ ./installer/bin/tiffcrop 'PATH_TO_TEST_DIR/CVE-2016-5323.tif' 'PATH_TO_TEST_DIR/out.tif'
## 273
#
# $ ./installer/bin/tiffcrop 'PATH_TO_TEST_DIR/CVE-2016-3991.tif' 'PATH_TO_TEST_DIR/out.tif'
## 274
#
# $ ./installer/bin/rgb2ycbcr -c zip -r 0 -h 0 -v 2 'PATH_TO_TEST_DIR/CVE-2016-3624.tif 'PATH_TO_TEST_DIR/out.tif'
## 277
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/1.tiff' -o 'PATH_TO_TEST_DIR/test.pdf'

## 281
#
# $ ./installer/bin/tiffinfo -d 'PATH_TO_TEST_DIR/ShowTile_heap-oob.tif'
## 282
#
# $ cp 'PATH_TO_TEST_DIR/19_tiffset.tiff' 'PATH_TO_TEST_DIR/19_tiffset2.tiff'
# $ ./installer/bin/tiffset 'PATH_TO_TEST_DIR/19_tiffset2.tiff'
## 283

## 286
#
# $ ./installer/bin/tiffset 'PATH_TO_TEST_DIR/19_tiffset.tiff'

## 287
#
# $ ./installer/bin/tiffcrop 'PATH_TO_TEST_DIR/2016-11-10-heap-buffer-overflow.tif' out

## 288

## 289

## 290

## 291
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/testcase' -o 'PATH_TO_TEST_DIR/test.pdf'

## 292
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/testcase' -o 'PATH_TO_TEST_DIR/test.pdf'

## 293
#
# $ ./installer/bin/tiff2bw 'PATH_TO_TEST_DIR/2016-11-16-tiff2bw-invalid-read.tif' 'PATH_TO_TEST_DIR/out'

## 295
#
# $ ./installer/bin/tiffcp 'PATH_TO_TEST_DIR/testcase'  out

## 296

## 297
#
# $ ./installer/bin/tiffcp 'PATH_TO_TEST_DIR/00071-libtiff-heapoverflow-_TIFFmemcpy'  out

## 298
#
# $ ./installer/bin/tiffcp -i 'PATH_TO_TEST_DIR/00074-libtiff-heapoverflow-TIFFFillStrip'  out

## 299
#
# $ ./installer/bin/tiffmedia 'PATH_TO_TEST_DIR/00083-libtiff-fpe-OJPEGDecodeRaw' out

## 300
#
# $ ./installer/bin/tiffcrop -i 'PATH_TO_TEST_DIR/00100-libtiff-heapoverflow-_TIFFFax3fillruns' out

## 301
#
# $ ./installer/bin/tiffcrop -i 'PATH_TO_TEST_DIR/00101-libtiff-heapoverflow-combineSeparateSamples16bits' out

## 302

## 303
#
# $ ./installer/bin/tiffinfo -Dijr 'PATH_TO_TEST_DIR/00101-libtiff-heapoverflow-combineSeparateSamples16bits'

## 304
#
# $ ./installer/bin/tiffinfo -Dijr 'PATH_TO_TEST_DIR/00101-libtiff-heapoverflow-combineSeparateSamples16bits'

## 305
#
# $ ./installer/bin/tiffcp -i 'PATH_TO_TEST_DIR/00067-libtiff-heapoverflow-tiffcp' out

## 306

## 307

## 308
#
# $ ./installer/bin/tiffcp -i 'PATH_TO_TEST_DIR/00072-libtiff-assert-readSeparateTilesIntoBuffer' out

## 309
#
# $ ./installer/bin/tiff2ps'PATH_TO_TEST_DIR/00108-libtiff-heapoverflow-PSDataBW' out
## 310
#
# $ ./installer/bin/tiff2ps 'PATH_TO_TEST_DIR/00107-libtiff-heapoverflow-PSDataColorContig' out
## 311
#
# $ ./installer/bin/tiff2pdf -j 'PATH_TO_TEST_DIR/testcase' -o out
## 312
#
# $ ./installer/bin/tiff2rgba 'PATH_TO_TEST_DIR/ycbcr_14_lzw.tif' out
## 313
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/00110-libtiff-memcpy-param-overlap-_TIFFmemcpy' -o out
## 314
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/00111-libtiff-invalidread-t2p_writeproc' -o out
## 315
#
# $ ./installer/bin/tiff2pdf 'PATH_TO_TEST_DIR/00112-libtiff-heapoverflow-_TIFFmemcpy' -o out
