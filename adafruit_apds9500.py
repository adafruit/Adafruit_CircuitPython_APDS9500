# The MIT License (MIT)
#
# Copyright (c) 2020 Bryan Siepert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_apds9500`
================================================================================
Library for the APDS9500 Gesture Sensor

* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

* Adafruit's APDS9500 Breakout: https://adafruit.com/product/44XX

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards: https://circuitpython.org/downloads
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_APDS9500.git"
import adafruit_bus_device.i2c_device as i2c_device
from adafruit_register.i2c_struct import UnaryStruct
from adafruit_register.i2c_bits import ROBits

#pylint:disable=invalid-name
#pylint:disable=too-many-instance-attributes
#pylint:disable=too-many-statements
#pylint:disable=too-few-public-methods

# _APDS9500_DEFAULT_ADDRESS = 0x00 # APDS9500 default i2c address
# _APDS9500_DEVICE_ID = 0xFF # APDS9500 device identifier


APDS9500_R_RegBankSet = 0xEF

# Bank 0*/
APDS9500_PartID_L = 0x00
APDS9500_PartID_H = 0x01
APDS9500_VersionID = 0x02

# Cursor Mode Controls */
APDS9500_R_CursorUseTop = 0x32
APDS9500_R_PositionFilterStartSizeTh_L = 0x33
APDS9500_R_PositionFilterStartSizeTh_H = 0x34
APDS9500_R_ProcessFilterStartSizeTh_L = 0x35
APDS9500_R_ProcessFilterStartSizeTh_H = 0x36
APDS9500_R_CursorClampLeft = 0x37
APDS9500_R_CursorClampRight = 0x38
APDS9500_R_CursorClampUp = 0x39
APDS9500_R_CursorClampDown = 0x3A
APDS9500_R_CursorClampCenterX_L = 0x3B
APDS9500_R_CursorClampCenterX_H = 0x3C
APDS9500_R_CursorClampCenterY_L = 0x3D
APDS9500_R_CursorClampCenterY_H = 0x3E
APDS9500_R_Cursor_ObjectSizeTh = 0x8B
APDS9500_R_PositionResolution = 0x8C

# Interrupt Controls */
APDS9500_R_MCU_Int_Flag = 0x40
APDS9500_R_Int1_En = 0x41
APDS9500_R_Int2_En = 0x42
APDS9500_Int_Flag_1 = 0x43
APDS9500_Int_Flag_2 = 0x44

# AE/AG Controls */
APDS9500_R_AELedOff_UB = 0x46
APDS9500_R_AELedOff_LB = 0x47
APDS9500_R_AE_Exposure_UB_L = 0x48
APDS9500_R_AE_Exposure_UB_H = 0x49
APDS9500_R_AE_Exposure_LB_L = 0x4A
APDS9500_R_AE_Exposure_LB_H = 0x4B
APDS9500_R_AE_Gain_UB = 0x4C
APDS9500_R_AE_Gain_LB = 0x4D
APDS9500_R_AE_Gain_Step = 0x4E
APDS9500_R_AE_Gain_Default = 0x4F
APDS9500_R_Exp_Sel = 0x50
APDS9500_R_Manual = 0x51
APDS9500_AG_Stage_GG = 0x54
APDS9500_Reg_ExposureNum_L = 0x55
APDS9500_Reg_ExposureNum_H = 0x56
APDS9500_Reg_global = 0x57
APDS9500_AE_LED_Off_YAvg = 0x58
APDS9500_AE_Dec_Inc = 0x59
APDS9500_AE_Normal_Factor = 0x5A

# GPIO Setting*/
APDS9500_InputMode_GPIO_0_1 = 0x80
APDS9500_InputMode_GPIO_2_3 = 0x81
APDS9500_InputMode_INT = 0x82

# Gesture Mode Controls */
APDS9500_R_LightThd = 0x83
APDS9500_R_GestureStartTh_L = 0x84
APDS9500_R_GestureStartTh_H = 0x85
APDS9500_R_GestureEndTh_L = 0x86
APDS9500_R_GestureEndTh_H = 0x87
APDS9500_R_ObjectMinZ = 0x88
APDS9500_R_ObjectMaxZ = 0x89
APDS9500_R_ProcessResolution = 0x8C
APDS9500_R_TimeDelayNum = 0x8D
APDS9500_R_Disable45Degree = 0x8E
APDS9500_R_XtoYGain = 0x8F
APDS9500_R_NoMotionCountThd = 0x90
APDS9500_R_NoObjectCountThd = 0x91
APDS9500_R_NormalizedImageWidth = 0x92
APDS9500_R_XDirectionThd = 0x93
APDS9500_R_YDirectionThd = 0x94
APDS9500_R_ZDirectionThd = 0x95
APDS9500_R_ZDirectionXYThd = 0x96
APDS9500_R_ZDirectionAngleThd = 0x97
APDS9500_R_RotateAngleThd = 0x98
APDS9500_R_RotateConti = 0x99
APDS9500_R_RotateXYThd = 0x9A
APDS9500_R_RotateZThd = 0x9B
APDS9500_R_Filter = 0x9C
APDS9500_R_DistThd = 0x9D
APDS9500_R_GestureDetEn = 0x9F
APDS9500_R_FilterImage = 0xA5
APDS9500_R_DiffAngleThd = 0xA9
APDS9500_ObjectCenterX_L = 0xAC
APDS9500_ObjectCenterX_H = 0xAD
APDS9500_ObjectCenterY_L = 0xAE
APDS9500_ObjectCenterY_H = 0xAF
APDS9500_ObjectAvgY = 0xB0
APDS9500_ObjectSize_L = 0xB1
APDS9500_ObjectSize_H = 0xB2
APDS9500_Gx = 0xB3
APDS9500_Gy = 0xB4
APDS9500_Gy = 0xB5
APDS9500_GestureResult = 0xB6
APDS9500_WaveCount = 0xB7
APDS9500_NoObjectCount = 0xB8
APDS9500_NoMotionCount = 0xB9
APDS9500_LightCount = 0xBA
APDS9500_LightAcc_L = 0xBB
APDS9500_LightAcc_H = 0xBC
APDS9500_TimeAcc_L = 0xBD
APDS9500_TimeAcc_H = 0xBE
APDS9500_AngleAcc_L = 0xC7
APDS9500_AngleAcc_H = 0xC8
APDS9500_XGainValue = 0xCA
APDS9500_YGainValue = 0xCB
APDS9500_R_YtoZSum = 0xCC
APDS9500_R_YtoZFactor = 0xCD
APDS9500_R_FilterLength = 0xCE
APDS9500_R_WaveThd = 0xCF
APDS9500_R_AbortCountThd = 0xD0
APDS9500_R_AbortLength = 0xD1
APDS9500_R_WaveEnH = 0xD2
APDS9500_PositionFilterCenterX_L = 0xD3
APDS9500_PositionFilterCenterXY_H = 0xD4
APDS9500_PositionFilterCenterY_L = 0xD5
APDS9500_PositionFilterAvgY_L = 0xD6
APDS9500_PositionFilterAvgY_H = 0xD7
APDS9500_PositionFilterSize_L = 0xD8
APDS9500_ProcessFilterAvgY_H = 0xD9
APDS9500_ProcessFilterCenterX_L = 0xDA
APDS9500_ProcessFilterCenterXY_H = 0xDB
APDS9500_ProcessFilterCenterY_L = 0xDC
APDS9500_ProcessFilterSize_L = 0xDD
APDS9500_ProcessFilterAvgY_L = 0xDE
APDS9500_AbortIntervalCount_L = 0xDF
APDS9500_unknown_1 = 0x5E
APDS9500_unknown_2 = 0x60

# bank 1
# Bank 1 */

# Image size settings */
APDS9500_Cmd_HSize = 0x00
APDS9500_Cmd_VSize = 0x01
APDS9500_Cmd_HStart = 0x02
APDS9500_Cmd_VStart = 0x03
APDS9500_Cmd_HV = 0x04
# Lens Shading */ =
APDS9500_R_LensShadingComp_EnH = 0x25
APDS9500_R_Offest_X = 0x26
APDS9500_R_Offest_Y = 0x27
APDS9500_R_LSC = 0x28
APDS9500_R_LSFT = 0x29
APDS9500_R_global = 0x42
APDS9500_R_ggh = 0x44
# Sleep Mode Parameters */ =
APDS9500_R_IDLE_TIME_L = 0x65
APDS9500_R_IDLE_TIME_H = 0x66
APDS9500_R_IDLE_TIME_SLEEP_1_L = 0x67
APDS9500_R_IDLE_TIME_SLEEP_1_H = 0x68
APDS9500_R_IDLE_TIME_SLEEP_2_L = 0x69
APDS9500_R_IDLE_TIME_SLEEP_2_H = 0x6A
APDS9500_R_Object_TIME_1_L = 0x6B
APDS9500_R_Object_TIME_1_H = 0x6C
APDS9500_R_Object_TIME_2_L = 0x6D
APDS9500_R_Object_TIME_2_H = 0x6E
APDS9500_R_TG_INIT_TIME = 0x6F
APDS9500_R_TG_POWERON_WAKEUP_TIME = 0x71
APDS9500_R_TG_EnH = 0x72
APDS9500_R_Auto_SLEEP_Mode = 0x73
APDS9500_R_Wake_Up_Sig_Sel = 0x74

# Image Controls */
APDS9500_R_SRAM_Read_EnH = 0x77
APDS9500_DEFAULT_ADDRESS = 0x73

class CV:
    """struct helper"""

    @classmethod
    def add_values(cls, value_tuples):
        "creates CV entires"
        cls.string = {}
        cls.lsb = {}

        for value_tuple in value_tuples:
            name, value, string, lsb = value_tuple
            setattr(cls, name, value)
            cls.string[value] = string
            cls.lsb[value] = lsb

    @classmethod
    def is_valid(cls, value):
        "Returns true if the given value is a member of the CV"
        return value in cls.string

class GestureResult(CV):
    """Possible results for ``gesture``"""
    pass #pylint: disable=unnecessary-pass

GestureResult.add_values((
    ('UP',  1, "Up", None),
    ('DOWN',  2, "Down", None),
    ('LEFT', 3, "Left", None),
    ('RIGHT', 4, "Right", None),
    ('FORWARD',  5, "Forward", None),
    ('BACKWARD', 6, "Backward", None),
    ('CLOCKWISE', 7, "Clockwise", None),
    ('COUNTERCLOCKWISE', 8, "Counterclockwise", None),
    ('WAVE', 9, "Wave", None)
))

class Gesture(CV):
    """Possible results for ``gesture``"""
    pass #pylint: disable=unnecessary-pass


Gesture.add_values((
    ('UP',  0x01, "Up", None),
    ('DOWN',  0x02, "Down", None),
    ('LEFT', 0x04, "Left", None),
    ('RIGHT', 0x08, "Right", None),
    ('FORWARD',  0x10, "Forward", None),
    ('BACKWARD', 0x20, "Backward", None),
    ('CLOCKWISE', 0x40, "Clockwise", None),
    ('COUNTERCLOCKWISE', 0x80, "Counterclockwise", None),
))


class APDS9500:
    """Library for the APDS9500 Gesture Sensor.

        :param ~busio.I2C i2c_bus: The I2C bus the APDS9500 is connected to.
        :param address: The I2C slave address of the sensor

    """

    # # endian/format helper
    # # b signed, 1 byte :: B unsigned 1 byte
    # # h signed, 2 bytes :: H unsigned 2 bytes
    # _raw_example_data = Struct(_APDS9500_EXAMPLE_XOUT_H, ">hhh")
    # _bank = RWBits(2, _APDS9500_REG_BANK_SEL, 4)
    # _reset = RWBit(_APDS9500_PWR_MGMT_1, 7)

    reg_bank_set = UnaryStruct(APDS9500_R_RegBankSet, ">B")
    cursor_clamp_left = UnaryStruct(APDS9500_R_CursorClampLeft, ">B")
    cursor_clamp_right = UnaryStruct(APDS9500_R_CursorClampRight, ">B")
    cursor_clamp_up = UnaryStruct(APDS9500_R_CursorClampUp, ">B")
    int2_en = UnaryStruct(APDS9500_R_Int2_En, ">B")
    ae_led_off_ub = UnaryStruct(APDS9500_R_AELedOff_UB, ">B")
    ae_led_off_lb = UnaryStruct(APDS9500_R_AELedOff_LB, ">B")
    ae_exposure_ub_l = UnaryStruct(APDS9500_R_AE_Exposure_UB_L, ">B")
    ae_exposure_ub_h = UnaryStruct(APDS9500_R_AE_Exposure_UB_H, ">B")
    ae_exposure_lb_l = UnaryStruct(APDS9500_R_AE_Exposure_LB_L, ">B")
    ae_gain_lb = UnaryStruct(APDS9500_R_AE_Gain_LB, ">B")
    manual = UnaryStruct(APDS9500_R_Manual, ">B")
    unknown_1 = UnaryStruct(APDS9500_unknown_1, ">B")
    unknown_2 = UnaryStruct(APDS9500_unknown_2, ">B")
    apds9500_input_mode_gpio_0_1 = UnaryStruct(APDS9500_InputMode_GPIO_0_1, ">B")
    apds9500_input_mode_gpio_2_3 = UnaryStruct(APDS9500_InputMode_GPIO_2_3, ">B")
    apds9500_input_mode_int = UnaryStruct(APDS9500_InputMode_INT, ">B")
    cursor_object_size_th = UnaryStruct(APDS9500_R_Cursor_ObjectSizeTh, ">B")
    no_motion_count_thd = UnaryStruct(APDS9500_R_NoMotionCountThd, ">B")
    z_direction_thd = UnaryStruct(APDS9500_R_ZDirectionThd, ">B")
    z_direction_xy_thd = UnaryStruct(APDS9500_R_ZDirectionXYThd, ">B")
    z_direction_angle_thd = UnaryStruct(APDS9500_R_ZDirectionAngleThd, ">B")
    rotate_xy_thd = UnaryStruct(APDS9500_R_RotateXYThd, ">B")
    filter = UnaryStruct(APDS9500_R_Filter, ">B")
    filter_image = UnaryStruct(APDS9500_R_FilterImage, ">B")
    yto_z_sum = UnaryStruct(APDS9500_R_YtoZSum, ">B")
    yto_z_factor = UnaryStruct(APDS9500_R_YtoZFactor, ">B")
    filter_length = UnaryStruct(APDS9500_R_FilterLength, ">B")
    wave_thd = UnaryStruct(APDS9500_R_WaveThd, ">B")
    abort_count_thd = UnaryStruct(APDS9500_R_AbortCountThd, ">B")
    reg_bank_set = UnaryStruct(APDS9500_R_RegBankSet, ">B")

    cmd_h_start = UnaryStruct(APDS9500_Cmd_HStart, ">B")
    cmd_v_start = UnaryStruct(APDS9500_Cmd_VStart, ">B")
    cmd_hv = UnaryStruct(APDS9500_Cmd_HV, ">B")
    lens_shading_comp_en_h = UnaryStruct(APDS9500_R_LensShadingComp_EnH, ">B")
    offest_y = UnaryStruct(APDS9500_R_Offest_Y, ">B")
    lsc = UnaryStruct(APDS9500_R_LSC, ">B")
    lsft = UnaryStruct(APDS9500_R_LSFT, ">B")
    cursor_clamp_center_y_h = UnaryStruct(APDS9500_R_CursorClampCenterY_H, ">B")
    unknown_1 = UnaryStruct(APDS9500_unknown_1, ">B")
    idle_time_l = UnaryStruct(APDS9500_R_IDLE_TIME_L, ">B")
    idle_time_sleep_1_l = UnaryStruct(APDS9500_R_IDLE_TIME_SLEEP_1_L, ">B")
    idle_time_sleep_2_l = UnaryStruct(APDS9500_R_IDLE_TIME_SLEEP_2_L, ">B")
    idle_time_sleep_2_h = UnaryStruct(APDS9500_R_IDLE_TIME_SLEEP_2_H, ">B")
    object_time_2_l = UnaryStruct(APDS9500_R_Object_TIME_2_L, ">B")
    object_time_2_h = UnaryStruct(APDS9500_R_Object_TIME_2_H, ">B")
    tg_en_h = UnaryStruct(APDS9500_R_TG_EnH, ">B")
    auto_sleep_mode = UnaryStruct(APDS9500_R_Auto_SLEEP_Mode, ">B")
    wake_up_sig_sel = UnaryStruct(APDS9500_R_Wake_Up_Sig_Sel, ">B")
    sram_read_en_h = UnaryStruct(APDS9500_R_SRAM_Read_EnH, ">B")

    # readers
    gestures_enabled = UnaryStruct(APDS9500_R_GestureDetEn, ">B")
    gesture_result_register = UnaryStruct(APDS9500_GestureResult, ">B")
    gesture_result = ROBits(4, APDS9500_GestureResult, 0)

    # 0 GestureResult 0xB6 3:0 - R Gesture result

    int_flag_1 = UnaryStruct(APDS9500_Int_Flag_1, ">B")
    int_flag_2 = UnaryStruct(APDS9500_Int_Flag_2, ">B")

    def __init__(self, i2c_bus, address=APDS9500_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)

        self.reg_bank_set = 0x00
        self.reg_bank_set = 0x00
        self.reg_bank_set = 0x0

        self.cursor_clamp_left = 0x7
        self.cursor_clamp_right = 0x17
        self.cursor_clamp_up = 0x6
        
        self.int2_en = 0x1
        
        self.ae_led_off_ub = 0x2D
        self.ae_led_off_lb = 0xF
        self.ae_exposure_ub_l = 0x3C
        self.ae_exposure_ub_h = 0x0
        self.ae_exposure_lb_l = 0x1E
        self.ae_gain_lb = 0x20
        
        self.manual = 0x10
        self.unkown_1 = 0x10
        self.unknown_2 = 0x27
        
        self.apds9500_input_mode_gpio_0_1 = 0x42
        self.apds9500_input_mode_gpio_2_3 = 0x44
        self.apds9500_input_mode_int = 0x4
        
        self.cursor_object_size_th = 0x1
        
        self.no_motion_count_thd = 0x6
        
        self.z_direction_thd = 0xA
        self.z_direction_xy_thd = 0xC
        self.z_direction_angle_thd = 0x5
        
        self.rotate_xy_thd = 0x14
        
        self.filter = 0x3F
        self.filter_image = 0x19
        
        self.yto_z_sum = 0x19
        self.yto_z_factor = 0xB
        
        self.filter_length = 0x3
        
        self.wave_thd = 0x64
        self.abort_count_thd = 0x21
        self.reg_bank_set = 0x1
        
        self.cmd_h_start = 0xF
        self.cmd_v_start = 0x10
        self.cmd_hv = 0x2
        
        self.lens_shading_comp_en_h = 0x1
        self.offest_y = 0x39
        self.lsc = 0x7F
        self.lsft = 0x8
        self.cursor_clamp_center_y_h = 0xFF
        self.unknown_1 = 0x3D
        
        self.idle_time_l = 0x96
        self.idle_time_sleep_1_l = 0x97
        self.idle_time_sleep_2_l = 0xCD
        self.idle_time_sleep_2_h = 0x1
        
        self.object_time_2_l = 0x2C
        self.object_time_2_h = 0x1
        
        self.tg_en_h = 0x1
        self.auto_sleep_mode = 0x35
        self.wake_up_sig_sel = 0x0
        self.sram_read_en_h = 0x1

        self.reg_bank_set = 0x00


    @property
    def gesture(self):
        detected_gestures = {}
        gesture_flag = self.int_flag_1

        if gesture_flag & Gesture.UP:
            detected_gestures[Gesture.UP] = True
        if gesture_flag & Gesture.DOWN:
            detected_gestures[Gesture.DOWN] = True
        if gesture_flag & Gesture.LEFT:
            detected_gestures[Gesture.LEFT] = True
        if gesture_flag & Gesture.RIGHT:
            detected_gestures[Gesture.RIGHT] = True
        if gesture_flag & Gesture.FORWARD:
            detected_gestures[Gesture.FORWARD] = True
        if gesture_flag & Gesture.BACKWARD:
            detected_gestures[Gesture.BACKWARD] = True
        if gesture_flag & Gesture.CLOCKWISE:
            detected_gestures[Gesture.CLOCKWISE] = True

        return detected_gestures