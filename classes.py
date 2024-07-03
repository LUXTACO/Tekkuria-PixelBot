from typing import Union, Tuple
from dataclasses import dataclass
from overlay_lib.classes import Vector2D, RgbaColor, RgbaGradient

@dataclass
class Entity:
    width: int
    height: int
    distance: int
    
    coords: Vector2D
    center_coords: Vector2D
    head_coords: Vector2D
    torso_coords: Vector2D
    legs_coords: Vector2D
    penis_coords: Vector2D

@dataclass
class DrawSettings:
    fill: bool
    filltype: str
    outlinecolor: RgbaColor
    fillcolor: Union[RgbaGradient, RgbaColor]
 
@dataclass
class Config:
    targetfps: int
    
    togglekey: int
    holdkey: int
    
    fovsize: int
    triggerfov: int
    minarea: int
    mindistance: int
    
    smoothing: float
    similarity: int
    autoshoot: bool
    
    targetbone: str
    headoffset: float
    torsooffset: float
    legsoffset: float
    penisoffset: float
    targetcolor: Tuple[int, int, int]
    
    drawbox: bool
    boxsettings: DrawSettings
    
    drawbone: bool
    bonesettings: DrawSettings
    
    drawfov: bool
    fovsettings: DrawSettings
    
    drawlines:bool
    linescolor: RgbaColor
    
    VALID_TARGET_SETTINGS = ["center_coords", "head_coords", "torso_coords", "legs_coords", "penis_coords"]
    
    def __post_init__(self):
        if self.targetbone not in self.VALID_TARGET_SETTINGS:
            raise ValueError(f"Invalid target_setting: {self.targetbone}. Must be one of {self.VALID_TARGET_SETTINGS}")

@dataclass
class KeyCode: 
    rightclick: int = 0x02
    sidebackbutton: int = 0x05
    sideforwardbutton: int = 0x06
    controlkey: int = 0x11
    shiftkey: int = 0x10
    altkey: int = 0x12
    spacebar: int = 0x20
    enterkey: int = 0x0D
    escapekey: int = 0x1B
    leftarrow: int = 0x25
    uparrow: int = 0x26
    rightarrow: int = 0x27
    downarrow: int = 0x28
    
    