import csv
import math
import random
from PIL import Image

"""
I converted the Arduino C++ that ran my 2020 and 2021
Christmas displays into the Python below.

WARNING: Questionable programming follows.

Actually, I take that back. There are a number of
elegant algorithms and processes that I shamelessly
appropriated that go uncredited because I didn't think
to include credit in the C++ written with the assumption
no one other tham me would ever see it.

Many thanks to those that let me stand on their shoulders
to build some interesting displays.

I have made NO ATTEMPT to optimize, simplify, or follow any
reasonable coding style. Example: global? Seriously? 
The goal was to get it working ONCE.
"""

level_num = 11
leds = [ ]
state = [ ]
frame = 0

max_milliamps = 0

brightmap = [
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
    1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
    2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
    5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
   10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
   17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
   25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
   37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
   51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
   69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
   90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
  115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
  144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
  177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
  215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255 ]



def clear_tree():
    global state
    for i in range(0,len(state)):
        state[i] = (0,0,0)

def hsv_to_rgb(h, s, v):
    if s == 0.0: v*=255; return (v, v, v)
    i = int(h*6.) # XXX assume int() truncates!
    f = (h*6.)-i
    p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f))))
    v*=255
    i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

def twinkle(huebase):
    global state
    for i in range(0,NUM_TREE):
        hue = ((random.randint(0, 32) + huebase) % 360) / 360
        saturation = 1
        brightness = brightmap[brightmap[brightmap[random.randint(0, 255)]]] / 255.0
        (r, g, b) = hsv_to_rgb(hue, saturation, brightness)
        state[i] = (int(round(r,0)), int(round(g,0)), int(round(b,0)))

def image(i,pix, width, height, frames):
    global state
    ratio = i / frames
    for i in range(0,NUM_TREE):
        dw = (led_string[i]['x'] + ratio)
        dh = led_string[i]['y']
        dx = int(round((dw * (width - 1)) % (width - 1),0))
        dy = int(round((dh * (height - 1)) % (height - 1),0))
        try:
            (r, g, b) = pix[dx,dy]
        except TypeError:
            palette = pix.getpalette()
            pixel = pix.getpixel((dx,dy))
            try:
                r = palette[pixel * 3]
                g = palette[pixel * 3 + 1]
                b = palette[pixel * 3 + 2]
            except TypeError:
                (r, g, b, a) = pixel
        state[i] = (int(r * 1.0),int(g * 1.0),int(b * 1.0))

def animated_image(i,im, width, height, img_frames, frames):
    global state
    ratio = i / frames
    for i in range(0,NUM_TREE):
        dw = (led_string[i]['x'] + ratio)
        dh = led_string[i]['y']
        dx = int(round((dw * (width - 1)) % (width - 1),0))
        dy = int(round((dh * (height - 1)) % (height - 1),0))
        (r, g, b) = pix[dx,dy]
        state[i] = (int(r * 1.0),int(g * 1.0),int(b * 1.0))

def candycane(frame):
    global state

    white = (192,192,192)
    red = (192,0,0)

    n3 = int(NUM_TREE/3)
    n6 = int(NUM_TREE/6)
    n12 = int(NUM_TREE/12)
    for i in range(0,n6):
        j0 = (frame + i + NUM_TREE - n12) % NUM_TREE
        j1 = (j0 + n6) % NUM_TREE
        j2 = (j1 + n6) % NUM_TREE
        j3 = (j2 + n6) % NUM_TREE
        j4 = (j3 + n6) % NUM_TREE
        j5 = (j4 + n6) % NUM_TREE
        state[j0] = white
        state[j1] = red
        state[j2] = white
        state[j3] = red
        state[j4] = white
        state[j5] = red

def sparkle3(col1,col2,col3,ratio):
    import random
    global state
    color = col1
    for i in range(0,NUM_TREE):
        choice = random.randint(0, 2)
        if choice == 0:
            color = col1
        elif choice == 1:
            color = col2
        else:
            color = col3
        if random.randint(0,65535) < ratio:
            state[i] = color
        else:
            state[i] = (0,0,0)

def set_level_color(level,color,source,clear=False):
    global state
    for i in source:
        if i['level'] == level:
            state[i['order_abs']-1] = color
        elif clear:
            state[i['order_abs']-1] = (0,0,0)

def frame_output(frame,state,led_order,brightness_control=False):
    global max_milliamps
    output = [ None ] * len(state)
    for i in range(0,len(state)):
        (r, g, b) = state[i]
        if brightness_control:
            r = brightmap[r]
            g = brightmap[g]
            b = brightmap[b]
        output[led_order[i]-1] = (r, g, b)
    row = [item for t in output for item in t]

    milliamps = 0
    for r in row:
        milliamps = milliamps + ((r/255) * 20)
    if milliamps > max_milliamps:
        max_milliamps = milliamps

    row.insert(0,frame)
    return row

with open('coords_2021.csv', mode='r', encoding='utf-8-sig') as csvfile:
    reader = csv.reader(csvfile)
    i = 1
    for row in reader:
        led = {
            'x': float(row[0]),
            'y': float(row[1]),
            'z': float(row[2]),
            'theta': None,
            'level': None,
            'order': i,
            'order_abs': None,
            'order_level': None,
        }
        led['theta'] = ((math.degrees(math.atan2(led['y'], led['x'])) % 360) - 90) % 360
        led['x'] = (360 - led['theta']) / 360
        leds.append(led)
        i = i + 1

#thetas = [x['theta'] for x in leds]
z_max = max([x['z'] for x in leds])
z_diff = z_max / level_num

for led in leds:
    led['y'] = (z_max - led['z']) / z_max
    led['level'] = int(round(math.ceil((led['z'] + 0.00000001)/ z_diff),0))
    if led['level'] > level_num:
        led['level'] = level_num

NUM_TREE = len(leds)

for i in range(0,NUM_TREE):
    state.append((0,0,0))

clear_tree()

levels = { }

for led in leds:
    try:
        levels[led['level']].append(led)
    except:
        levels[led['level']] = [ led ]

level_leds = { }
for level in levels:
    levels[level] = sorted(levels[level], key = lambda i: i['theta'])
    level_leds[level] = len(levels[level])

accum_level_leds = [ ]
accum = 0
for i in range(1,level_num+1):
    accum_level_leds.append(accum + level_leds[i])
    accum = accum_level_leds[-1]

led_string = [ ]
abs_order = 1
for level in range(1,level_num+1):
    level_order = 1
    for led in levels[level]:
        led['order_abs'] = abs_order
        led['order_level'] = level_order
        led_string.append(led)
        abs_order = abs_order + 1
        level_order = level_order + 1

led_string = sorted(led_string, key = lambda i: i['order_abs'])

#for x in led_string:
#    print(x)

header = """FRAME_ID,R_0,G_0,B_0,R_1,G_1,B_1,R_2,G_2,B_2,R_3,G_3,B_3,R_4,G_4,B_4,R_5,G_5,B_5,R_6,G_6,B_6,R_7,G_7,B_7,R_8,G_8,B_8,R_9,G_9,B_9,R_10,G_10,B_10,R_11,G_11,B_11,R_12,G_12,B_12,R_13,G_13,B_13,R_14,G_14,B_14,R_15,G_15,B_15,R_16,G_16,B_16,R_17,G_17,B_17,R_18,G_18,B_18,R_19,G_19,B_19,R_20,G_20,B_20,R_21,G_21,B_21,R_22,G_22,B_22,R_23,G_23,B_23,R_24,G_24,B_24,R_25,G_25,B_25,R_26,G_26,B_26,R_27,G_27,B_27,R_28,G_28,B_28,R_29,G_29,B_29,R_30,G_30,B_30,R_31,G_31,B_31,R_32,G_32,B_32,R_33,G_33,B_33,R_34,G_34,B_34,R_35,G_35,B_35,R_36,G_36,B_36,R_37,G_37,B_37,R_38,G_38,B_38,R_39,G_39,B_39,R_40,G_40,B_40,R_41,G_41,B_41,R_42,G_42,B_42,R_43,G_43,B_43,R_44,G_44,B_44,R_45,G_45,B_45,R_46,G_46,B_46,R_47,G_47,B_47,R_48,G_48,B_48,R_49,G_49,B_49,R_50,G_50,B_50,R_51,G_51,B_51,R_52,G_52,B_52,R_53,G_53,B_53,R_54,G_54,B_54,R_55,G_55,B_55,R_56,G_56,B_56,R_57,G_57,B_57,R_58,G_58,B_58,R_59,G_59,B_59,R_60,G_60,B_60,R_61,G_61,B_61,R_62,G_62,B_62,R_63,G_63,B_63,R_64,G_64,B_64,R_65,G_65,B_65,R_66,G_66,B_66,R_67,G_67,B_67,R_68,G_68,B_68,R_69,G_69,B_69,R_70,G_70,B_70,R_71,G_71,B_71,R_72,G_72,B_72,R_73,G_73,B_73,R_74,G_74,B_74,R_75,G_75,B_75,R_76,G_76,B_76,R_77,G_77,B_77,R_78,G_78,B_78,R_79,G_79,B_79,R_80,G_80,B_80,R_81,G_81,B_81,R_82,G_82,B_82,R_83,G_83,B_83,R_84,G_84,B_84,R_85,G_85,B_85,R_86,G_86,B_86,R_87,G_87,B_87,R_88,G_88,B_88,R_89,G_89,B_89,R_90,G_90,B_90,R_91,G_91,B_91,R_92,G_92,B_92,R_93,G_93,B_93,R_94,G_94,B_94,R_95,G_95,B_95,R_96,G_96,B_96,R_97,G_97,B_97,R_98,G_98,B_98,R_99,G_99,B_99,R_100,G_100,B_100,R_101,G_101,B_101,R_102,G_102,B_102,R_103,G_103,B_103,R_104,G_104,B_104,R_105,G_105,B_105,R_106,G_106,B_106,R_107,G_107,B_107,R_108,G_108,B_108,R_109,G_109,B_109,R_110,G_110,B_110,R_111,G_111,B_111,R_112,G_112,B_112,R_113,G_113,B_113,R_114,G_114,B_114,R_115,G_115,B_115,R_116,G_116,B_116,R_117,G_117,B_117,R_118,G_118,B_118,R_119,G_119,B_119,R_120,G_120,B_120,R_121,G_121,B_121,R_122,G_122,B_122,R_123,G_123,B_123,R_124,G_124,B_124,R_125,G_125,B_125,R_126,G_126,B_126,R_127,G_127,B_127,R_128,G_128,B_128,R_129,G_129,B_129,R_130,G_130,B_130,R_131,G_131,B_131,R_132,G_132,B_132,R_133,G_133,B_133,R_134,G_134,B_134,R_135,G_135,B_135,R_136,G_136,B_136,R_137,G_137,B_137,R_138,G_138,B_138,R_139,G_139,B_139,R_140,G_140,B_140,R_141,G_141,B_141,R_142,G_142,B_142,R_143,G_143,B_143,R_144,G_144,B_144,R_145,G_145,B_145,R_146,G_146,B_146,R_147,G_147,B_147,R_148,G_148,B_148,R_149,G_149,B_149,R_150,G_150,B_150,R_151,G_151,B_151,R_152,G_152,B_152,R_153,G_153,B_153,R_154,G_154,B_154,R_155,G_155,B_155,R_156,G_156,B_156,R_157,G_157,B_157,R_158,G_158,B_158,R_159,G_159,B_159,R_160,G_160,B_160,R_161,G_161,B_161,R_162,G_162,B_162,R_163,G_163,B_163,R_164,G_164,B_164,R_165,G_165,B_165,R_166,G_166,B_166,R_167,G_167,B_167,R_168,G_168,B_168,R_169,G_169,B_169,R_170,G_170,B_170,R_171,G_171,B_171,R_172,G_172,B_172,R_173,G_173,B_173,R_174,G_174,B_174,R_175,G_175,B_175,R_176,G_176,B_176,R_177,G_177,B_177,R_178,G_178,B_178,R_179,G_179,B_179,R_180,G_180,B_180,R_181,G_181,B_181,R_182,G_182,B_182,R_183,G_183,B_183,R_184,G_184,B_184,R_185,G_185,B_185,R_186,G_186,B_186,R_187,G_187,B_187,R_188,G_188,B_188,R_189,G_189,B_189,R_190,G_190,B_190,R_191,G_191,B_191,R_192,G_192,B_192,R_193,G_193,B_193,R_194,G_194,B_194,R_195,G_195,B_195,R_196,G_196,B_196,R_197,G_197,B_197,R_198,G_198,B_198,R_199,G_199,B_199,R_200,G_200,B_200,R_201,G_201,B_201,R_202,G_202,B_202,R_203,G_203,B_203,R_204,G_204,B_204,R_205,G_205,B_205,R_206,G_206,B_206,R_207,G_207,B_207,R_208,G_208,B_208,R_209,G_209,B_209,R_210,G_210,B_210,R_211,G_211,B_211,R_212,G_212,B_212,R_213,G_213,B_213,R_214,G_214,B_214,R_215,G_215,B_215,R_216,G_216,B_216,R_217,G_217,B_217,R_218,G_218,B_218,R_219,G_219,B_219,R_220,G_220,B_220,R_221,G_221,B_221,R_222,G_222,B_222,R_223,G_223,B_223,R_224,G_224,B_224,R_225,G_225,B_225,R_226,G_226,B_226,R_227,G_227,B_227,R_228,G_228,B_228,R_229,G_229,B_229,R_230,G_230,B_230,R_231,G_231,B_231,R_232,G_232,B_232,R_233,G_233,B_233,R_234,G_234,B_234,R_235,G_235,B_235,R_236,G_236,B_236,R_237,G_237,B_237,R_238,G_238,B_238,R_239,G_239,B_239,R_240,G_240,B_240,R_241,G_241,B_241,R_242,G_242,B_242,R_243,G_243,B_243,R_244,G_244,B_244,R_245,G_245,B_245,R_246,G_246,B_246,R_247,G_247,B_247,R_248,G_248,B_248,R_249,G_249,B_249,R_250,G_250,B_250,R_251,G_251,B_251,R_252,G_252,B_252,R_253,G_253,B_253,R_254,G_254,B_254,R_255,G_255,B_255,R_256,G_256,B_256,R_257,G_257,B_257,R_258,G_258,B_258,R_259,G_259,B_259,R_260,G_260,B_260,R_261,G_261,B_261,R_262,G_262,B_262,R_263,G_263,B_263,R_264,G_264,B_264,R_265,G_265,B_265,R_266,G_266,B_266,R_267,G_267,B_267,R_268,G_268,B_268,R_269,G_269,B_269,R_270,G_270,B_270,R_271,G_271,B_271,R_272,G_272,B_272,R_273,G_273,B_273,R_274,G_274,B_274,R_275,G_275,B_275,R_276,G_276,B_276,R_277,G_277,B_277,R_278,G_278,B_278,R_279,G_279,B_279,R_280,G_280,B_280,R_281,G_281,B_281,R_282,G_282,B_282,R_283,G_283,B_283,R_284,G_284,B_284,R_285,G_285,B_285,R_286,G_286,B_286,R_287,G_287,B_287,R_288,G_288,B_288,R_289,G_289,B_289,R_290,G_290,B_290,R_291,G_291,B_291,R_292,G_292,B_292,R_293,G_293,B_293,R_294,G_294,B_294,R_295,G_295,B_295,R_296,G_296,B_296,R_297,G_297,B_297,R_298,G_298,B_298,R_299,G_299,B_299,R_300,G_300,B_300,R_301,G_301,B_301,R_302,G_302,B_302,R_303,G_303,B_303,R_304,G_304,B_304,R_305,G_305,B_305,R_306,G_306,B_306,R_307,G_307,B_307,R_308,G_308,B_308,R_309,G_309,B_309,R_310,G_310,B_310,R_311,G_311,B_311,R_312,G_312,B_312,R_313,G_313,B_313,R_314,G_314,B_314,R_315,G_315,B_315,R_316,G_316,B_316,R_317,G_317,B_317,R_318,G_318,B_318,R_319,G_319,B_319,R_320,G_320,B_320,R_321,G_321,B_321,R_322,G_322,B_322,R_323,G_323,B_323,R_324,G_324,B_324,R_325,G_325,B_325,R_326,G_326,B_326,R_327,G_327,B_327,R_328,G_328,B_328,R_329,G_329,B_329,R_330,G_330,B_330,R_331,G_331,B_331,R_332,G_332,B_332,R_333,G_333,B_333,R_334,G_334,B_334,R_335,G_335,B_335,R_336,G_336,B_336,R_337,G_337,B_337,R_338,G_338,B_338,R_339,G_339,B_339,R_340,G_340,B_340,R_341,G_341,B_341,R_342,G_342,B_342,R_343,G_343,B_343,R_344,G_344,B_344,R_345,G_345,B_345,R_346,G_346,B_346,R_347,G_347,B_347,R_348,G_348,B_348,R_349,G_349,B_349,R_350,G_350,B_350,R_351,G_351,B_351,R_352,G_352,B_352,R_353,G_353,B_353,R_354,G_354,B_354,R_355,G_355,B_355,R_356,G_356,B_356,R_357,G_357,B_357,R_358,G_358,B_358,R_359,G_359,B_359,R_360,G_360,B_360,R_361,G_361,B_361,R_362,G_362,B_362,R_363,G_363,B_363,R_364,G_364,B_364,R_365,G_365,B_365,R_366,G_366,B_366,R_367,G_367,B_367,R_368,G_368,B_368,R_369,G_369,B_369,R_370,G_370,B_370,R_371,G_371,B_371,R_372,G_372,B_372,R_373,G_373,B_373,R_374,G_374,B_374,R_375,G_375,B_375,R_376,G_376,B_376,R_377,G_377,B_377,R_378,G_378,B_378,R_379,G_379,B_379,R_380,G_380,B_380,R_381,G_381,B_381,R_382,G_382,B_382,R_383,G_383,B_383,R_384,G_384,B_384,R_385,G_385,B_385,R_386,G_386,B_386,R_387,G_387,B_387,R_388,G_388,B_388,R_389,G_389,B_389,R_390,G_390,B_390,R_391,G_391,B_391,R_392,G_392,B_392,R_393,G_393,B_393,R_394,G_394,B_394,R_395,G_395,B_395,R_396,G_396,B_396,R_397,G_397,B_397,R_398,G_398,B_398,R_399,G_399,B_399,R_400,G_400,B_400,R_401,G_401,B_401,R_402,G_402,B_402,R_403,G_403,B_403,R_404,G_404,B_404,R_405,G_405,B_405,R_406,G_406,B_406,R_407,G_407,B_407,R_408,G_408,B_408,R_409,G_409,B_409,R_410,G_410,B_410,R_411,G_411,B_411,R_412,G_412,B_412,R_413,G_413,B_413,R_414,G_414,B_414,R_415,G_415,B_415,R_416,G_416,B_416,R_417,G_417,B_417,R_418,G_418,B_418,R_419,G_419,B_419,R_420,G_420,B_420,R_421,G_421,B_421,R_422,G_422,B_422,R_423,G_423,B_423,R_424,G_424,B_424,R_425,G_425,B_425,R_426,G_426,B_426,R_427,G_427,B_427,R_428,G_428,B_428,R_429,G_429,B_429,R_430,G_430,B_430,R_431,G_431,B_431,R_432,G_432,B_432,R_433,G_433,B_433,R_434,G_434,B_434,R_435,G_435,B_435,R_436,G_436,B_436,R_437,G_437,B_437,R_438,G_438,B_438,R_439,G_439,B_439,R_440,G_440,B_440,R_441,G_441,B_441,R_442,G_442,B_442,R_443,G_443,B_443,R_444,G_444,B_444,R_445,G_445,B_445,R_446,G_446,B_446,R_447,G_447,B_447,R_448,G_448,B_448,R_449,G_449,B_449,R_450,G_450,B_450,R_451,G_451,B_451,R_452,G_452,B_452,R_453,G_453,B_453,R_454,G_454,B_454,R_455,G_455,B_455,R_456,G_456,B_456,R_457,G_457,B_457,R_458,G_458,B_458,R_459,G_459,B_459,R_460,G_460,B_460,R_461,G_461,B_461,R_462,G_462,B_462,R_463,G_463,B_463,R_464,G_464,B_464,R_465,G_465,B_465,R_466,G_466,B_466,R_467,G_467,B_467,R_468,G_468,B_468,R_469,G_469,B_469,R_470,G_470,B_470,R_471,G_471,B_471,R_472,G_472,B_472,R_473,G_473,B_473,R_474,G_474,B_474,R_475,G_475,B_475,R_476,G_476,B_476,R_477,G_477,B_477,R_478,G_478,B_478,R_479,G_479,B_479,R_480,G_480,B_480,R_481,G_481,B_481,R_482,G_482,B_482,R_483,G_483,B_483,R_484,G_484,B_484,R_485,G_485,B_485,R_486,G_486,B_486,R_487,G_487,B_487,R_488,G_488,B_488,R_489,G_489,B_489,R_490,G_490,B_490,R_491,G_491,B_491,R_492,G_492,B_492,R_493,G_493,B_493,R_494,G_494,B_494,R_495,G_495,B_495,R_496,G_496,B_496,R_497,G_497,B_497,R_498,G_498,B_498,R_499,G_499,B_499"""
header = header.split(",")
led_order = [x['order'] for x in led_string]

bc_on = True

if True:
    max_milliamps = 0
    clear_tree()
    with open('examples/td_01_35fps_candycane.csv', mode='w', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for i in range(0,500):
            candycane(i)
            row = frame_output(i,state,led_order,brightness_control=bc_on)
            writer.writerow(row)
    print("candycane Max milliamps: ", max_milliamps)

if True:
    max_milliamps = 0
    clear_tree()
    with open('examples/td_02_35fps_sparkle.csv', mode='w', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for i in range(0,500):
            sparkle3((255,255,255), (255,0,0), (0,255,0), 1000)
            row = frame_output(i,state,led_order)
            writer.writerow(row)
    print("sparkle Max milliamps: ", max_milliamps)

if True:
    max_milliamps = 0
    clear_tree()
    black = (0,0,0)
    white = (192,192,192)
    red = (216,0,0)
    with open('examples/td_03_35fps_levels.csv', mode='w', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        i = 0
        for pancake_level in range(1,level_num+1):
            for lvl in range(level_num,pancake_level-1,-1):
                if lvl < level_num:
                    set_level_color(lvl+1,black,source=led_string,clear=False)
                if lvl % 2:
                    color = red
                else:
                    color = white
                set_level_color(lvl,color,source=led_string,clear=False)
                for x in range(0,3):
                    row = frame_output(i+x,state,led_order,brightness_control=bc_on)
                    writer.writerow(row)
                i = i + 3
        
        for x in range(0,6):
            row = frame_output(i+x,state,led_order,brightness_control=bc_on)
            writer.writerow(row)
        i = i + 6

        for pancake_level in range(1,level_num+1):
            for lvl in range(pancake_level,-1,-1):
                set_level_color(lvl,black,source=led_string,clear=False)
                if lvl > 1:
                    if lvl % 2:
                        color = red
                    else:
                        color = white
                    set_level_color(lvl-1,color,source=led_string,clear=False)
                    for x in range(0,3):
                        row = frame_output(i+x,state,led_order,brightness_control=bc_on)
                        writer.writerow(row)
                i = i + 3
    print("levels milliamps: ", max_milliamps)

if True:
    max_milliamps = 0
    huebase = 90
    clear_tree()
    with open('examples/td_04_35fps_twinkle.csv', mode='w', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for i in range(0,6000):
            if random.randint(0, 3) == 0:
                huebase = (huebase - 1) % 360
            twinkle(huebase)
            row = frame_output(i,state,led_order)
            writer.writerow(row)
            if huebase == 91:
                break
    print("twinkle milliamps: ", max_milliamps)

if True:
    max_milliamps = 0
    clear_tree()
    with Image.open('src/globe.webp') as im:
        pix = im.load()
        (width, height) = im.size
        with open('examples/td_05_35fps_globe.csv', mode='w', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for i in range(0,350):
                image(i,pix,width,height,350)
                row = frame_output(i,state,led_order,brightness_control=bc_on)
                writer.writerow(row)
    print("globe milliamps: ", max_milliamps)

if True:
    max_milliamps = 0
    clear_tree()
    with Image.open('src/mosaic_before.jpg') as im:
        pix = im.load()
        (width, height) = im.size
        with open('examples/td_06_35fps_matts_favorite_spreadsheet.csv', mode='w', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for i in range(0,350):
                image(i,pix,width,height,350)
                row = frame_output(i,state,led_order,brightness_control=False)
                writer.writerow(row)
    print("spreadsheet milliamps: ", max_milliamps)

if False:
    max_milliamps = 0
    clear_tree()
    with Image.open('src/twitter_avatar.jpg') as im:
        pix = im.load()
        (width, height) = im.size
        with open('examples/td_xx_35fps_twitter_avatar.csv', mode='w', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for i in range(0,350):
                image(i,pix,width,height,350)
                row = frame_output(i,state,led_order)
                writer.writerow(row)
    print("avatar milliamps: ", max_milliamps)

if True:
    store = [ ]
    max_milliamps = 0
    clear_tree()
    with Image.open('src/g0kw.gif') as im:
        (width, height) = im.size
        with open('examples/td_07_35fps_fractal.csv', mode='w', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            last = 0
            for i in range(20,265):
                frame = i
                im.seek(frame)
                image(i,im,width,height,350)
                row = frame_output(i-20,state,led_order,brightness_control=bc_on)
                store.insert(0,row)
                writer.writerow(row)
                last = i - 20
            i = 0
            for row in store:
                row = [last + i] + row[1:]
                writer.writerow(row)
                i = i + 1
    print("fractal milliamps: ", max_milliamps)