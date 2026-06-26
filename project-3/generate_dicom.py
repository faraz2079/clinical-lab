import datetime
import numpy as np
import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import generate_uid, ExplicitVRLittleEndian

meta = Dataset()
meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.2"
meta.MediaStorageSOPInstanceUID = generate_uid()
meta.TransferSyntaxUID = ExplicitVRLittleEndian

ds = FileDataset("sample.dcm", {}, file_meta=meta, preamble=b"\0" * 128)
ds.is_implicit_VR = False
ds.is_little_endian = True

ds.PatientName = "Test^Patient"
ds.PatientID = "12345"
ds.PatientBirthDate = "19800101"
ds.PatientSex = "M"

ds.StudyInstanceUID = generate_uid()
ds.StudyDate = datetime.date.today().strftime("%Y%m%d")
ds.StudyTime = datetime.datetime.now().strftime("%H%M%S")
ds.StudyDescription = "Test CT Study"
ds.AccessionNumber = ""

ds.SeriesInstanceUID = generate_uid()
ds.SeriesNumber = 1
ds.Modality = "CT"

ds.SOPClassUID = meta.MediaStorageSOPClassUID
ds.SOPInstanceUID = meta.MediaStorageSOPInstanceUID
ds.InstanceNumber = 1

ds.Rows = 64
ds.Columns = 64
ds.BitsAllocated = 16
ds.BitsStored = 16
ds.HighBit = 15
ds.PixelRepresentation = 0
ds.SamplesPerPixel = 1
ds.PhotometricInterpretation = "MONOCHROME2"
ds.PixelData = np.zeros((64, 64), dtype=np.uint16).tobytes()

pydicom.dcmwrite("sample.dcm", ds)
print("Created sample.dcm")
