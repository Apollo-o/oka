import ffmpeg
import cv2
import os


class muse:

    def __init__(self, base_path, total_episodes, status="normal"):

        self.base_path = base_path
        self.imports = 0
        self.flag = -1
        self.modes = (128, 256)

        self.ffmpeg = "./dependencies/ffmpeg.exe"
        self.exif = r".\dependencies\exiftool.exe"

        if os.path.isdir(base_path) and base_path[-1] == "/":
            self.file_database = sorted(
                [f"{base_path}{idx}" for idx in os.listdir(
                    base_path) if idx.endswith(".mp4")], key=len)

            self.setup_permissions(self.modes[0])
            self.setup_files()

            self.find_missing_episodes(total_episodes)
            self.find_corruption()
            self.find_duplicates_cmp()
            self.find_duplicates_hash()
            self.find_metadata()

            if status.lower().strip() == "enhance":
                self.find_enhance()

            self.setup_permissions(self.modes[-1])

        else:
            print(f"[!] Invalid Directory: {self.base_path}")
            exit(0)

    def setup_permissions(self, code):
        os.chmod(self.base_path, code)
        for file in self.file_database:
            os.chmod(file, code)

    def setup_files(self):

        temp = []
        for idx, file in enumerate(self.file_database, start=1):
            new_file = f"{self.base_path}{idx}.mp4"
            if not (os.path.exists(new_file)):
                os.rename(file, new_file)
            temp.append(new_file)

        self.file_database = temp

    def change_title(self, title):

        if input(f"Continue [yes][{title.rstrip(
                "-")}-{self.file_database[0].split("/")[-1]}]: ") != 'yes':
            exit(0)

        for file in self.file_database:

            base = file.split("/")
            new_title = f"{f"{"/".join(
                base[:-1])}/"}{title.rstrip("-")}-{base[-1]}"

            if not (os.path.exists(new_title)):
                os.rename(file, new_title)

    def find_missing_episodes(self, total_episodes):

        count = 0
        ep_values = list(range(1, total_episodes+1))
        for idx, file in enumerate(self.file_database):

            ep_num = int(file.split("/")[-1][:-4])

            if ep_num in ep_values:
                ep_values.remove(ep_num)
            if idx == len(self.file_database)-1:
                amount = len(self.file_database)-total_episodes

                if amount < 0:
                    print(f"[!] Missing {amount} | "
                          f"Episodes {ep_values}")
                    count += 1
                elif amount > 0:
                    print(f"[!] Extra +{amount} | " +
                          f"Episodes {[
                            total_episodes + num for num in range(
                                1, amount+1)]}")
                    count += 1

        if count == 0:
            print("[miss]\tNo missing episodes")
            self.flag = 0
        else:
            self.flag = -1

    def find_duplicates_cmp(self):

        if self.flag == 0:

            from filecmp import cmp

            duplicates = []
            for idx1, file in enumerate(self.file_database):

                for element in self.file_database:

                    if file == element:
                        pass
                    elif cmp(file, element, shallow=False):

                        value1 = file.split("/")[-1][:-4]
                        value2 = element.split("/")[-1][:-4]

                        if not (
                            f"{value1},{value2}" in duplicates) and not (
                                value2 in str(duplicates)):
                            duplicates.append(f"{value1}:{value2}")

            if not (duplicates):
                print("[cmp]\tNo duplicate episodes")
                self.flag = 0
            else:
                print(f"[cmp]\t{duplicates}")
                self.flag = -1

    def find_duplicates_hash(self, seconds=300):

        if self.flag == 0:

            from PIL.Image import fromarray
            from imagehash import phash

            frames = []
            for path in self.file_database:

                video = cv2.VideoCapture(path)
                video.set(
                    cv2.CAP_PROP_POS_FRAMES, int(
                        video.get(cv2.CAP_PROP_FPS)) * seconds)

                try:
                    frames.append(phash(fromarray(video.read()[1])))
                except:
                    frames.append(None)

                video.release()

            duplicates = []
            for val1, frame1 in enumerate(frames, start=1):
                for val2, frame2 in enumerate(frames, start=1):
                    if frame1 and frame2 is not None:
                        if val1 != val2 and (frame1 - frame2) < 0.9:
                            if not (
                                f"{val1}:{val2}" in duplicates) and not (
                                    str(val2) in str(duplicates)):
                                duplicates.append(f"{val1}:{val2}")

            if not (duplicates):
                print("[hash]\tNo duplicate episodes")
                self.flag = 0
            else:
                print(f"[hash]\t{duplicates}")
                self.flag = -1

    def find_corruption(self):

        if self.flag == 0:

            count = 0
            for file in self.file_database:

                file_out = f"{file[:-4]}_.mp4"

                try:

                    status = self.check_error(
                        count, file, ffmpeg.input(file).output(
                            file_out, f="mp4", vcodec="copy", acodec="copy"
                            ).run(capture_stderr=True, cmd=self.ffmpeg
                                  )[-1], file_out)

                except ffmpeg._run.Error as e:

                    status = self.check_error(count, file, e.stderr, file_out)

                if status == 1:
                    count += 1
                else:

                    os.remove(file)
                    os.rename(file_out, file)

            if count == 0:
                print("[corr]\tNo corrupt episodes")
                self.flag = 0

    def check_error(self, count, file, info, file_out):

        error = str(info, 'utf-8').lower()
        if "error" in error or "invalid" in error:
            print(
                f"[!] Corrupt | Episode {file.split(
                    "/")[-1][:-4]}")
            os.remove(file_out)
            self.flag = -1
            return 1

    def find_metadata(self):

        if self.flag == 0:

            run = f"{self.exif} -ext mp4 -all= {self.base_path}*.mp4 >&1 > nul"

            try:
                status = str(
                    os.system(
                        run)
                    ).lower()
            except PermissionError:
                status = "error"

            [os.remove(f"{self.base_path}{idx}"
                       ) for idx in os.listdir(
                           self.base_path) if idx.endswith("_original")]

            if status == "0" or status.find("error") != -1:
                print("[exif]\tNo metadata left")
                self.flag = 0
            else:
                self.flag = -1

    def find_enhance(self):

        if self.flag == 0:

            from multiprocessing import cpu_count, Pool

            self.imports = (cpu_count()//2, Pool)
            files = [f"{self.base_path}temp_video.mp4",
                     f"{self.base_path}temp_audio.mp4",
                     f"{self.base_path}temp_output.mp4"]

            for idx1, file in enumerate(self.file_database):

                self.video_enhance(file, files[0])
                self.extract_audio(file, files[1])
                self.merge_files(files[0], files[1], files[2])
                os.replace(files[2], file)

            with open(files[2], 'w'):
                pass

            self.delete_files(files)
            print("[cv2]\tNo denoise left")

        else:
            self.flag = -1

    def video_enhance(self, path, output):

        video = cv2.VideoCapture(path)
        writer = cv2.VideoWriter(output,
                                 cv2.VideoWriter_fourcc(*"mp4v"),
                                 video.get(cv2.CAP_PROP_FPS),
                                 (int(video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                  int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        chunks = self.get_chunks(int(video.get(cv2.CAP_PROP_FRAME_COUNT)))

        for idx, chunk in enumerate(chunks):

            if idx == len(chunks)-1:
                break

            frames = []
            for element in range(chunks[idx], chunks[idx+1]):

                frames.append(video.read()[-1])

            files = self.denoise_multiprocess(frames)

            for file in files:
                writer.write(file)

        video.release()
        writer.release()

    def get_chunks(self, frames):

        chunks = []
        for idx in range(1, frames, frames//10):
            chunks.append(idx)
        return chunks + [(frames - chunks[-1]) + chunks[-1]]

    def denoise_multiprocess(self, frames):
        with self.imports[1](processes=self.imports[0]) as pool:
            return pool.map(self.denoise_frame, frames)

    def denoise_frame(self, frame):
        return cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 5)

    def extract_audio(self, file, output):
        ffmpeg.input(file).output(
            output, vn=None, acodec="copy").run(
                capture_stderr=True, cmd=self.ffmpeg, overwrite_output=True)

    def merge_files(self, video, audio, output):
        ffmpeg.output(ffmpeg.input(video),
                      ffmpeg.input(audio),
                      output, vcodec="copy",
                      acodec="copy").run(
                          capture_stderr=True, cmd=self.ffmpeg,
                          overwrite_output=True)

    def delete_files(self, files):
        try:
            [os.remove(file) for file in files]
        except OSError:
            pass
