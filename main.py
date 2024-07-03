import os
import cv2
import time
import json
import dxcam
import win32api
import threading
import numpy as np
from classes import *
from interface import * 
from overlay_lib import *

class PixelBot:
    
    KEYCODES = {0x02: 'rightclick', 0x05: 'sidebackbutton', 0x06: 'sideforwardbutton', 0x11: 'controlkey', 0x10: 'shiftkey', 0x12: 'altkey', 0x20: 'spacebar', 0x0D: 'enterkey', 0x1B: 'escapekey', 0x25: 'leftarrow', 0x26: 'uparrow', 0x27: 'rightarrow', 0x28: 'downarrow'}
    
    def __init__(self):
        if os.path.exists('./configs/config.json'):
            with open('./configs/config.json', 'r') as file:
                json_config = json.load(file)
        else:
            json_config = {
                "targetfps": 240,
                "togglekey": "sidebackbutton",
                "holdkey": "rightclick",
                "fovsize": 400,
                "triggerfov": 20,
                "minarea": 85,
                "mindistance":50,
                "smoothing": 1,
                "similarity": 80,
                "autoshoot": False,
                "targetbone": "head_coords",
                "headoffset": 0.25,
                "torsooffset": 0.05,
                "legsoffset": 0.13,
                "penisoffset": 0.25,
                "targetcolor": [255, 0, 213],
                "drawbox": True,
                "boxsettings": {
                    "fill": True,
                    "filltype": "gradient",
                    "outlinecolor": [255, 55, 0, 255],
                    "fillcolor": ([255, 55, 0, 10], [255, 55, 0, 40]),
                },
                "drawbone": True,
                "bonesettings": {
                    "fill": True,
                    "filltype": "gradient",
                    "outlinecolor": [255, 55, 0, 255],
                    "fillcolor": ([255, 55, 0, 10], [255, 55, 0, 40]),
                },
                "drawfov": True,
                "fovsettings": {
                    "fill": False,
                    "filltype": "gradient",
                    "outlinecolor": [255, 55, 0, 255],
                    "fillcolor": ([255, 55, 0, 10], [255, 55, 0, 40]),
                },
                "drawlines":False,
                "linescolor": [255, 55, 0, 255],
            }
            
            with open('./configs/config.json', 'w') as file:
                json.dump(json_config, file, indent=4)
                
        self.config = Config(
            targetfps=int(json_config['targetfps']),
            togglekey=getattr(KeyCode, json_config['togglekey']),
            holdkey=getattr(KeyCode, json_config['holdkey']),
            fovsize=json_config['fovsize'],
            triggerfov=json_config['triggerfov'],
            minarea=json_config['minarea'],
            mindistance=json_config['mindistance'],
            smoothing=json_config['smoothing'],
            similarity=json_config['similarity'],
            autoshoot=json_config['autoshoot'],
            targetbone=json_config['targetbone'],
            headoffset=json_config['headoffset'],
            torsooffset=json_config['torsooffset'],
            legsoffset=json_config['legsoffset'],
            penisoffset=json_config['penisoffset'],
            targetcolor=tuple(json_config['targetcolor']),
            drawbox=json_config['drawbox'],
            boxsettings=DrawSettings(
                fill=json_config['boxsettings']['fill'],
                filltype=json_config['boxsettings']['filltype'],
                outlinecolor=RgbaColor(*json_config['boxsettings']['outlinecolor']),
                fillcolor=RgbaGradient(
                    RgbaColor(*json_config['boxsettings']['fillcolor'][0]),
                    RgbaColor(*json_config['boxsettings']['fillcolor'][1])
                ) if json_config['boxsettings']['filltype'] == 'gradient' else RgbaColor(*json_config['boxsettings']['fillcolor']),
            ),
            drawbone=json_config['drawbone'],
            bonesettings=DrawSettings(
                fill=json_config['bonesettings']['fill'],
                filltype=json_config['bonesettings']['filltype'],
                outlinecolor=RgbaColor(*json_config['bonesettings']['outlinecolor']),
                fillcolor=RgbaGradient(
                    RgbaColor(*json_config['bonesettings']['fillcolor'][0]),
                    RgbaColor(*json_config['bonesettings']['fillcolor'][1])
                ) if json_config['bonesettings']['filltype'] == 'gradient' else RgbaColor(*json_config['bonesettings']['fillcolor']),
            ),
            drawfov=json_config['drawfov'],
            fovsettings=DrawSettings(
                fill=json_config['fovsettings']['fill'],
                filltype=json_config['fovsettings']['filltype'],
                outlinecolor=RgbaColor(*json_config['fovsettings']['outlinecolor']),
                fillcolor=RgbaGradient(
                    RgbaColor(*json_config['fovsettings']['fillcolor'][0]),
                    RgbaColor(*json_config['fovsettings']['fillcolor'][1])
                ) if json_config['fovsettings']['filltype'] == 'gradient' else RgbaColor(*json_config['fovsettings']['fillcolor']),
            ),
            drawlines=json_config['drawlines'],
            linescolor=RgbaColor(*json_config['linescolor'])
        )
        
        self.entity_list = []
        self.aim_toggle = False
        self.pause_mainloop = False
        
        self.screen_center = Vector2D(int((win32api.GetSystemMetrics(0))/2), int((win32api.GetSystemMetrics(1))/2))
        self.screen_size = Vector2D(win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1))
    
    def MainLoop(self):
        self.color_range = [
            np.array(
                [
                    self.config.targetcolor[0] - self.config.similarity, 
                    self.config.targetcolor[1] - self.config.similarity, 
                    self.config.targetcolor[2] - self.config.similarity
                ]
            ), 
            np.array(
                [
                    self.config.targetcolor[0] + self.config.similarity, 
                    self.config.targetcolor[1] + self.config.similarity, 
                    self.config.targetcolor[2] + self.config.similarity
                ]
            )
        ]
        
        self.capture_region = (
            int(self.screen_center.x - self.config.fovsize),
            int(self.screen_center.y - self.config.fovsize),
            int(self.screen_center.x + self.config.fovsize),
            int(self.screen_center.y + self.config.fovsize)
        )
        
        self.last_target = None
        
        self.camera = dxcam.create()
        self.camera.start(target_fps=240, region=self.capture_region)

        while True:
            
            if self.pause_mainloop:
                while self.pause_mainloop:
                    time.sleep(0.01)
            
            latest_frame = self.camera.get_latest_frame()
            if win32api.GetAsyncKeyState(self.config.holdkey) != 0 or self.aim_toggle:
                self.entity_list = self.ScanFrame(latest_frame)
                
                if len(self.entity_list) < 1:
                    continue
                
                closest_entity = min(self.entity_list, key=lambda entity: entity.distance)
                
                self.PerformMove(x=getattr(closest_entity, self.config.targetbone).x, y=getattr(closest_entity, self.config.targetbone).y)

                self.last_target = closest_entity
            else:
                time.sleep(0.01)
            
            if win32api.GetAsyncKeyState(self.config.togglekey) != 0:
                self.aim_toggle = not self.aim_toggle
                time.sleep(0.5)
      
    def ScanFrame(self, frame):
        
        found_entities = []
        
        mindistance = self.config.mindistance
        minarea = self.config.minarea
        capture_region = self.capture_region
        screen_center = self.screen_center
        
        headoffset = self.config.headoffset
        torsooffset = self.config.torsooffset
        legsoffset = self.config.legsoffset
        penisoffset = self.config.penisoffset
        
        targets = cv2.inRange(frame, self.color_range[0], self.color_range[1])
        target_contours, _ = cv2.findContours(targets, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in target_contours:
            area = cv2.contourArea(contour)
            if area > minarea:
                x, y, w, h = cv2.boundingRect(contour)
                x += capture_region[0]
                y += capture_region[1]
                
                new_entity = Entity(
                    width=w,
                    height=h,
                    distance=np.sqrt((x - screen_center.x)**2 + (y - screen_center.y)**2),
                    coords=Vector2D(x, y),
                    center_coords=Vector2D((x+w/2), (y+h/2)),
                    head_coords=Vector2D((x+w/2), ((y+h/2)-round(h*headoffset))),
                    torso_coords=Vector2D((x+w/2), ((y+h/2)-round(h*torsooffset))),
                    legs_coords=Vector2D((x+w/2), ((y+h/2)+round(h/legsoffset))),
                    penis_coords=Vector2D((x+w/2), ((y+h/2)+round(h*penisoffset)))
                )
                
                
                if not any(np.sqrt((new_entity.coords.x - entity.coords.x)**2 + (new_entity.coords.y - entity.coords.y)**2) < mindistance for entity in found_entities):
                    found_entities.append(new_entity)
                
        return found_entities

    def PerformMove(self, x: int, y: int):
        movement_vector = Vector2D(
            int(round(((x - self.screen_center.x) * self.config.smoothing))),
            int(round(((y - self.screen_center.y) * self.config.smoothing)))
        )
        
        win32api.mouse_event(1, movement_vector.x, movement_vector.y, 0, 0) #> move
        
        if self.config.autoshoot:
            cursor_pos = win32api.GetCursorPos()
            if abs(cursor_pos[0] - x) <= self.config.triggerfov and abs(cursor_pos[1] - y) <= 15:
                win32api.mouse_event(2, 0, 0, 0, 0) #> click
                win32api.mouse_event(4, 0, 0, 0, 0) #> release
    
    def DrawCallback(self):
        draw_list = []
        
        if self.config.drawfov:
            if self.config.fovsettings.fill:
                draw_list.append(
                    FlDrawCircle(
                        coords=self.screen_center, 
                        radius=self.config.fovsize, 
                        fill_color=self.config.fovsettings.fillcolor, 
                        outline_color=self.config.fovsettings.outlinecolor, 
                        thickness=1
                    )
                )
            else:
                draw_list.append(
                    SkDrawCircle(
                        coords=self.screen_center, 
                        radius=self.config.fovsize, 
                        color=self.config.fovsettings.outlinecolor, 
                        thickness=1
                    )
                )
        
        for entity in self.entity_list:       
            if self.config.drawbox:
                if self.config.boxsettings.fill:
                    draw_list.append(
                        FlDrawRect(
                            coords=entity.coords, 
                            width=entity.width, 
                            height=entity.height, 
                            fill_color=self.config.boxsettings.fillcolor, 
                            outline_color=self.config.boxsettings.outlinecolor, 
                            thickness=1
                        )
                    )
                else:
                    draw_list.append(
                        SkDrawRect(
                            coords=entity.coords, 
                            width=entity.width, 
                            height=entity.height, 
                            color=self.config.boxsettings.outlinecolor, 
                            thickness=1
                        )
                    )
            if self.config.drawbone:
                if self.config.bonesettings.fill:
                    draw_list.append(
                        FlDrawCircle(
                            coords=getattr(entity, self.config.targetbone), 
                            radius=5, 
                            fill_color=self.config.bonesettings.fillcolor, 
                            outline_color=self.config.bonesettings.outlinecolor, 
                            thickness=1
                        )
                    )
                else:
                    draw_list.append(
                        SkDrawCircle(
                            coords=getattr(entity, self.config.targetbone), 
                            radius=5, 
                            color=self.config.bonesettings.outlinecolor, 
                            thickness=1
                        )
                    )
            
            if self.config.drawlines:
                draw_list.append(
                    DrawLine(
                        start_coord=self.screen_center,
                        end_coord=Vector2D(int(entity.coords.x+(entity.width/2)), int(entity.coords.y+entity.height)),
                        color=self.config.linescolor,
                        thickness=1
                    )
                )

        self.entity_list = []
        time.sleep(0.01)
                
        return draw_list
    
    def updateFOV(self, fovsize):
        self.config.fovsize = fovsize
        
        self.capture_region = (
            int(self.screen_center.x - self.config.fovsize),
            int(self.screen_center.y - self.config.fovsize),
            int(self.screen_center.x + self.config.fovsize),
            int(self.screen_center.y + self.config.fovsize)
        )
        
        self.pause_mainloop = True
        self.camera.stop()
        self.camera.start(target_fps=self.config.targetfps, region=self.capture_region)
        self.pause_mainloop = False
    
    def updateFPS(self, targetfps):
        self.config.targetfps = targetfps
        
        self.pause_mainloop = True
        self.camera.stop()
        self.camera.start(target_fps=self.config.targetfps, region=self.capture_region)
        self.pause_mainloop = False
    
    def updateColor(self, targetcolor=None, similarity=None):
        
        if similarity == None:
            similarity = self.config.similarity
            
        if targetcolor == None:
            targetcolor = self.config.targetcolor
            
        self.config.targetcolor = targetcolor
        self.config.similarity = similarity
        
        self.color_range = [
            np.array(
                [
                    self.config.targetcolor[0] - similarity, 
                    self.config.targetcolor[1] - similarity, 
                    self.config.targetcolor[2] - similarity
                ]
            ), 
            np.array(
                [
                    self.config.targetcolor[0] + similarity, 
                    self.config.targetcolor[1] + similarity, 
                    self.config.targetcolor[2] + similarity
                ]
            )
        ]
        
    def loadConfig(self, configname):
        try:
            
            configpath = f'./configs/{configname}'
            
            with open(configpath, 'r') as file:
                json_config = json.load(file)
                
            self.config = Config(
                targetfps=int(json_config['targetfps']),
                togglekey=getattr(KeyCode, json_config['togglekey']),
                holdkey=getattr(KeyCode, json_config['holdkey']),
                fovsize=json_config['fovsize'],
                triggerfov=json_config['triggerfov'],
                minarea=json_config['minarea'],
                mindistance=json_config['mindistance'],
                smoothing=json_config['smoothing'],
                similarity=json_config['similarity'],
                autoshoot=json_config['autoshoot'],
                targetbone=json_config['targetbone'],
                headoffset=json_config['headoffset'],
                torsooffset=json_config['torsooffset'],
                legsoffset=json_config['legsoffset'],
                penisoffset=json_config['penisoffset'],
                targetcolor=tuple(json_config['targetcolor']),
                drawbox=json_config['drawbox'],
                boxsettings=DrawSettings(
                    fill=json_config['boxsettings']['fill'],
                    filltype=json_config['boxsettings']['filltype'],
                    outlinecolor=RgbaColor(*json_config['boxsettings']['outlinecolor']),
                    fillcolor=RgbaGradient(
                        RgbaColor(*json_config['boxsettings']['fillcolor'][0]),
                        RgbaColor(*json_config['boxsettings']['fillcolor'][1])
                    ) if json_config['boxsettings']['filltype'] == 'gradient' else RgbaColor(*json_config['boxsettings']['fillcolor']),
                ),
                drawbone=json_config['drawbone'],
                bonesettings=DrawSettings(
                    fill=json_config['bonesettings']['fill'],
                    filltype=json_config['bonesettings']['filltype'],
                    outlinecolor=RgbaColor(*json_config['bonesettings']['outlinecolor']),
                    fillcolor=RgbaGradient(
                        RgbaColor(*json_config['bonesettings']['fillcolor'][0]),
                        RgbaColor(*json_config['bonesettings']['fillcolor'][1])
                    ) if json_config['bonesettings']['filltype'] == 'gradient' else RgbaColor(*json_config['bonesettings']['fillcolor']),
                ),
                drawfov=json_config['drawfov'],
                fovsettings=DrawSettings(
                    fill=json_config['fovsettings']['fill'],
                    filltype=json_config['fovsettings']['filltype'],
                    outlinecolor=RgbaColor(*json_config['fovsettings']['outlinecolor']),
                    fillcolor=RgbaGradient(
                        RgbaColor(*json_config['fovsettings']['fillcolor'][0]),
                        RgbaColor(*json_config['fovsettings']['fillcolor'][1])
                    ) if json_config['fovsettings']['filltype'] == 'gradient' else RgbaColor(*json_config['fovsettings']['fillcolor']),
                ),
                drawlines=json_config['drawlines'],
                linescolor=RgbaColor(*json_config['linescolor'])
            )
            
            self.updateColor()
            self.updateFOV(self.config.fovsize)
        except Exception as e:
            print(e)
            
    def saveConfig(self, configname):
        configpath = f'./configs/{configname}'
        with open(configpath, 'w') as file:
            json_config = {
                "targetfps": self.config.targetfps,
                "togglekey": self.KEYCODES[self.config.togglekey],
                "holdkey": self.KEYCODES[self.config.holdkey],
                "fovsize": self.config.fovsize,
                "triggerfov": self.config.triggerfov,
                "minarea": self.config.minarea,
                "mindistance": self.config.mindistance,
                "smoothing": self.config.smoothing,
                "similarity": self.config.similarity,
                "autoshoot": self.config.autoshoot,
                "targetbone": self.config.targetbone,
                "headoffset": self.config.headoffset,
                "torsooffset": self.config.torsooffset,
                "legsoffset": self.config.legsoffset,
                "penisoffset": self.config.penisoffset,
                "targetcolor": list(self.config.targetcolor),
                "drawbox": self.config.drawbox,
                "boxsettings": {
                    "fill": self.config.boxsettings.fill,
                    "filltype": self.config.boxsettings.filltype,
                    "outlinecolor": [self.config.boxsettings.outlinecolor.r, self.config.boxsettings.outlinecolor.g, self.config.boxsettings.outlinecolor.b, self.config.boxsettings.outlinecolor.a],
                    "fillcolor": (
                        [self.config.boxsettings.fillcolor.from_rgba.r, self.config.boxsettings.fillcolor.from_rgba.g, self.config.boxsettings.fillcolor.from_rgba.b, self.config.boxsettings.fillcolor.from_rgba.a],
                        [self.config.boxsettings.fillcolor.to_rgba.r,self.config.boxsettings.fillcolor.to_rgba.g, self.config.boxsettings.fillcolor.to_rgba.b, self.config.boxsettings.fillcolor.to_rgba.a]
                    ) if self.config.boxsettings.filltype == 'gradient' else [self.config.boxsettings.fillcolor.r, self.config.boxsettings.fillcolor.g, self.config.boxsettings.fillcolor.b, self.config.boxsettings.fillcolor.a],
                },
                "drawbone": self.config.drawbone,
                "bonesettings": {
                    "fill": self.config.bonesettings.fill,
                    "filltype": self.config.bonesettings.filltype,
                    "outlinecolor": [self.config.bonesettings.outlinecolor.r, self.config.bonesettings.outlinecolor.g, self.config.bonesettings.outlinecolor.b, self.config.bonesettings.outlinecolor.a],
                    "fillcolor": (
                        [self.config.bonesettings.fillcolor.from_rgba.r, self.config.bonesettings.fillcolor.from_rgba.g, self.config.bonesettings.fillcolor.from_rgba.b, self.config.bonesettings.fillcolor.from_rgba.a],
                        [self.config.bonesettings.fillcolor.to_rgba.r,self.config.bonesettings.fillcolor.to_rgba.g, self.config.bonesettings.fillcolor.to_rgba.b, self.config.bonesettings.fillcolor.to_rgba.a]
                    ) if self.config.bonesettings.filltype == 'gradient' else [self.config.bonesettings.fillcolor.r, self.config.bonesettings.fillcolor.g, self.config.bonesettings.fillcolor.b, self.config.bonesettings.fillcolor.a],
                },
                "drawfov": self.config.drawfov,
                "fovsettings": {
                    "fill": self.config.fovsettings.fill,
                    "filltype": self.config.fovsettings.filltype,
                    "outlinecolor": [self.config.fovsettings.outlinecolor.r, self.config.fovsettings.outlinecolor.g, self.config.fovsettings.outlinecolor.b, self.config.fovsettings.outlinecolor.a],
                    "fillcolor": (
                        [self.config.fovsettings.fillcolor.from_rgba.r, self.config.fovsettings.fillcolor.from_rgba.g, self.config.fovsettings.fillcolor.from_rgba.b, self.config.fovsettings.fillcolor.from_rgba.a],
                        [self.config.fovsettings.fillcolor.to_rgba.r,self.config.fovsettings.fillcolor.to_rgba.g, self.config.fovsettings.fillcolor.to_rgba.b, self.config.fovsettings.fillcolor.to_rgba.a]
                    ) if self.config.fovsettings.filltype == 'gradient' else [self.config.fovsettings.fillcolor.r, self.config.fovsettings.fillcolor.g, self.config.fovsettings.fillcolor.b, self.config.fovsettings.fillcolor.a],
                },
                "drawlines": self.config.drawlines,
                "linescolor": [self.config.linescolor.r, self.config.linescolor.g, self.config.linescolor.b, self.config.linescolor.a]
            }
            
            json.dump(json_config, file, indent=4)
            
    def getConfigFiles(self):
        base_path = './configs'
        rawpaths = os.listdir(base_path)
        files_info = []
        for path in rawpaths:
            if path.endswith('.json'):
                files_info.append({"filename": path, "filepath": os.path.join(base_path, path)})
        
        return files_info
    
    def deleteConfig(self, configname):
        if os.path.exists(f'./configs/{configname}'):
            configpath = f'./configs/{configname}'
            os.remove(configpath)
            
    def createConfig(self, configname):
        configpath = f'./configs/{configname}'
        with open(configpath, 'w') as file:
            json_config = {
                "targetfps": 240,
                "togglekey": "sidebackbutton",
                "holdkey": "rightclick",
                "fovsize": 400,
                "triggerfov": 20,
                "minarea": 85,
                "mindistance":50,
                "smoothing": 1,
                "similarity": 80,
                "autoshoot": False,
                "targetbone": "head_coords",
                "headoffset": 0.25,
                "torsooffset": 0.05,
                "legsoffset": 0.13,
                "penisoffset": 0.25,
                "targetcolor": [255, 0, 213],
                "drawbox": True,
                "boxsettings": {
                    "fill": True,
                    "filltype": "gradient",
                    "outlinecolor": [255, 55, 0, 255],
                    "fillcolor": ([255, 55, 0, 10], [255, 55, 0, 40]),
                },
                "drawbone": True,
                "bonesettings": {
                    "fill": True,
                    "filltype": "gradient",
                    "outlinecolor": [255, 55, 0, 255],
                    "fillcolor": ([255, 55, 0, 10], [255, 55, 0, 40]),
                },
                "drawfov": True,
                "fovsettings": {
                    "fill": False,
                    "filltype": "gradient",
                    "outlinecolor": [255, 55, 0, 255],
                    "fillcolor": ([255, 55, 0, 10], [255, 55, 0, 40]),
                },
                "drawlines":False,
                "linescolor": [255, 55, 0, 255]
            }
            
            json.dump(json_config, file, indent=4)

if __name__ == '__main__':
    pixelbot_instance = PixelBot()
    pixelbot_thread = threading.Thread(target=pixelbot_instance.MainLoop)
    pixelbot_thread.start()
    
    Overlay(drawlistCallback=pixelbot_instance.DrawCallback, guiWindow=GuiWindow, guiWindowArgs=pixelbot_instance, refreshTimeout=8).spawn()