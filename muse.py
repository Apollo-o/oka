# Author: o-o
# Date: 23/3/2025
# Description: Muse Class

import ffmpeg
import cv2
import os

class muse:
    def __init__(self, _b_, toepi, fgb_dyu_sdyu___="normal"):
        self.__sdau = _b_
        self.dsajbdjbas = 0
        self.cdsn = -1
        self.__nifd_ = (128, 256)
        self.djashsuhui = "./dependencies/ffmpeg.exe"
        self.gfdono = r".\dependencies\exiftool.exe"
        if os.path.isdir(_b_) and _b_[-1] == "/":
            self.__s32__ = sorted(
                [f"{_b_}{_n_}" for _n_ in os.listdir(
                    _b_) if _n_.endswith(".mp4")], key=len)
            self.__sias__(self.__nifd_[0])
            self.sdi_fds_s()
            self.gnfoni(toepi)
            self.dasnodaoi()
            self.sjbdja()
            self.hmfgih()
            self.mtfdgnd()
            if fgb_dyu_sdyu___.lower().strip() == "enhance":
                self.___bdiu_()
            self.__sias__(self.__nifd_[-1])
        else:
            print(f"[!] Invalid Directory: {self.__sdau}")
            exit(0)
    def __sias__(self, code):
        os.chmod(self.__sdau, code)
        for kphj_ in self.__s32__:
            os.chmod(kphj_, code)
    def sdi_fds_s(self):
        fdo_ = []
        for __aa__, _saaq__ in enumerate(self.__s32__, start=1):
            na_ = f"{self.__sdau}{__aa__}.mp4"
            if not (os.path.exists(na_)):
                os.rename(_saaq__, na_)
            fdo_.append(na_)
        self.__s32__ = fdo_
    def vgvas(self, k_):
        if input(f"Continue [yes][{k_.rstrip(
                "-")}-{self.__s32__[0].split("/")[-1]}]: ") != 'yes':
            exit(0)
        for vvsgd_ in self.__s32__:
            __biifd_ = vvsgd_.split("/")
            __idsuis__ = f"{f"{"/".join(
                __biifd_[:-1])}/"}{k_.rstrip("-")}-{__biifd_[-1]}"
            if not (os.path.exists(__idsuis__)):
                os.rename(vvsgd_, __idsuis__)
    def gnfoni(self, dsa_):
        ofdnv = 0
        fdsj_ = list(range(1, dsa_+1))
        for isudsiua, ons__ in enumerate(self.__s32__):
            jd0a = int(ons__.split("/")[-1][:-4])
            if jd0a in fdsj_:
                fdsj_.remove(jd0a)
            if isudsiua == len(self.__s32__)-1:
                ht0 = len(self.__s32__)-dsa_
                if ht0 < 0:
                    print(f"[!] Missing {ht0} | "
                          f"Episodes {fdsj_}")
                    ofdnv += 1
                elif ht0 > 0:
                    print(f"[!] Extra +{ht0} | " +
                          f"Episodes {[
                            dsa_ + h0gf for h0gf in range(
                                1, ht0+1)]}")
                    ofdnv += 1
        if ofdnv == 0:
            print("[miss]\tNo missing episodes")
            self.cdsn = 0
        else:
            self.cdsn = -1
    def sjbdja(self):
        if self.cdsn == 0:
            from filecmp import cmp
            oufd = []
            for jtryw, nfos in enumerate(self.__s32__):
                for dhasu in self.__s32__:
                    if nfos == dhasu:
                        pass
                    elif cmp(nfos, dhasu, shallow=False):
                        rj0t = nfos.split("/")[-1][:-4]
                        c83n8 = dhasu.split("/")[-1][:-4]
                        if not (
                            f"{rj0t},{c83n8}" in oufd) and not (
                                c83n8 in str(oufd)):
                            oufd.append(f"{rj0t}:{c83n8}")
            if not (oufd):
                print("[cmp]\tNo duplicate episodes")
                self.cdsn = 0
            else:
                print(f"[cmp]\t{oufd}")
                self.cdsn = -1
    def hmfgih(self, u67=300):
        if self.cdsn == 0:
            from PIL.Image import fromarray
            from imagehash import phash
            ntyi = []
            for u9u in self.__s32__:
                fe9rw = cv2.VideoCapture(u9u)
                fe9rw.set(
                    cv2.CAP_PROP_POS_FRAMES, int(
                        fe9rw.get(cv2.CAP_PROP_FPS)) * u67)
                try:
                    ntyi.append(phash(fromarray(fe9rw.read()[1])))
                except:
                    ntyi.append(None)
                fe9rw.release()
            bhvc = []
            for biire, bfhia in enumerate(ntyi, start=1):
                for tjoir, etre in enumerate(ntyi, start=1):
                    if bfhia and etre is not None:
                        if biire != tjoir and (bfhia - etre) < 0.9:
                            if not (
                                f"{biire}:{tjoir}" in bhvc) and not (
                                    str(tjoir) in str(bhvc)):
                                bhvc.append(f"{biire}:{tjoir}")
            if not (bhvc):
                print("[hash]\tNo duplicate episodes")
                self.cdsn = 0
            else:
                print(f"[hash]\t{bhvc}")
                self.cdsn = -1
    def dasnodaoi(self):
        if self.cdsn == 0:
            dbssa = 0
            for dsdou in self.__s32__:
                reoige = f"{dsdou[:-4]}_.mp4"
                try:
                    rte = self.jhgjt(
                        dbssa, dsdou, ffmpeg.input(dsdou).output(
                            reoige, f="mp4", vcodec="copy", acodec="copy"
                            ).run(capture_stderr=True, cmd=self.djashsuhui
                                  )[-1], reoige)
                except ffmpeg._run.Error as e:
                    rte = self.jhgjt(dbssa, dsdou, e.stderr, reoige)
                if rte == 1:
                    dbssa += 1
                else:
                    os.remove(dsdou)
                    os.rename(reoige, dsdou)
            if dbssa == 0:
                print("[corr]\tNo corrupt episodes")
                self.cdsn = 0
    def jhgjt(self, gffdgdf, vbdfiufd, fosndodon, fdnggndfogd):
        fsbdf = str(fosndodon, 'utf-8').lower()
        if "error" in fsbdf or "invalid" in fsbdf:
            print(
                f"[!] Corrupt | Episode {vbdfiufd.split(
                    "/")[-1][:-4]}")
            os.remove(fdnggndfogd)
            self.cdsn = -1
            return 1
    def mtfdgnd(self):
        if self.cdsn == 0:
            fdnsofoisd = f"{self.gfdono} -ext mp4 -all= {self.__sdau}*.mp4 >&1 > nul"
            try:
                sdoa = str(
                    os.system(
                        fdnsofoisd)
                    ).lower()
            except PermissionError:
                sdoa = "error"
            [os.remove(f"{self.__sdau}{hidfsdf}"
                       ) for hidfsdf in os.listdir(
                           self.__sdau) if hidfsdf.endswith("_original")]
            if sdoa == "0" or sdoa.find("error") != -1:
                print("[exif]\tNo metadata left")
                self.cdsn = 0
            else:
                self.cdsn = -1
    def ___bdiu_(self):
        if self.cdsn == 0:
            from multiprocessing import cpu_count, Pool
            self.dsajbdjbas = (cpu_count()//2, Pool)
            nfigidg__ = [f"{self.__sdau}temp_video.mp4",
                     f"{self.__sdau}temp_audio.mp4",
                     f"{self.__sdau}temp_output.mp4"]
            for _sdn_un_, gf_dg_ in enumerate(self.__s32__):
                self.__bdsfsa__(gf_dg_, nfigidg__[0])
                self.__fdsands__(gf_dg_, nfigidg__[1])
                self.sfdd__u_a_(nfigidg__[0], nfigidg__[1], nfigidg__[2])
                os.replace(nfigidg__[2], gf_dg_)
            with open(nfigidg__[2], 'w'):
                pass
            self.dd__dsa__(nfigidg__)
            print("[cv2]\tNo denoise left")
        else:
            self.cdsn = -1
    def __bdsfsa__(self, __dw_qn_, __bd__aib__):
        _as__id__ = cv2.VideoCapture(__dw_qn_)
        _dc_s__js = cv2.VideoWriter(__bd__aib__,
                                 cv2.VideoWriter_fourcc(*"mp4v"),
                                 _as__id__.get(cv2.CAP_PROP_FPS),
                                 (int(_as__id__.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                  int(_as__id__.get(cv2.CAP_PROP_FRAME_HEIGHT))))
        s_b__ = self.i___b__(int(_as__id__.get(cv2.CAP_PROP_FRAME_COUNT)))
        for _df_ad__, jbsad in enumerate(s_b__):
            if _df_ad__ == len(s_b__)-1:
                break
            _dsf_s_ = []
            for element in range(s_b__[_df_ad__], s_b__[_df_ad__+1]):
                _dsf_s_.append(_as__id__.read()[-1])
            _d_s__ = self._cdkkc_a_(_dsf_s_)
            for __ssghds__ in _d_s__:
                _dc_s__js.write(__ssghds__)
        _as__id__.release()
        _dc_s__js.release()
    def i___b__(self, bjd):
        __gfdst_ = []
        for idx in range(1, bjd, bjd//10):
            __gfdst_.append(idx)
        return __gfdst_ + [(bjd - __gfdst_[-1]) + __gfdst_[-1]]
    def _cdkkc_a_(self, i_df__):
        with self.dsajbdjbas[1](processes=self.dsajbdjbas[0]) as pool:
            return pool.map(self.d__da__, i_df__)
    def d__da__(self, n_ofd__):
        return cv2.fastNlMeansDenoisingColored(n_ofd__, None, 10, 10, 7, 5)
    def __fdsands__(self, sa____nfddo, s_aj__):
        ffmpeg.input(sa____nfddo).output(
            s_aj__, vn=None, acodec="copy").run(
                capture_stderr=True, cmd=self.djashsuhui, overwrite_output=True)
    def sfdd__u_a_(self, dsnidos_, _sa_p_, sn_a_os_):
        ffmpeg.output(ffmpeg.input(dsnidos_),
                      ffmpeg.input(_sa_p_),
                      sn_a_os_, vcodec="copy",
                      acodec="copy").run(
                          capture_stderr=True, cmd=self.djashsuhui,
                          overwrite_output=True)
    def dd__dsa__(self, _f_d_):
        try:
            [os.remove(_dddddd_) for _dddddd_ in _f_d_]
        except OSError:
            pass