import sys
import os
import json
import shutil
import subprocess
import time
import webbrowser
from xml.etree.ElementTree import tostring
from xmlrpc.client import boolean
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from datetime import date

from ui_unturned_dedicated_server_window import Ui_Form

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setFixedSize(375, 425)
        self.setWindowIcon(QIcon("icon/unturned.png"))

        #【使用前聲明】
        about = QMessageBox()
        about.setText("【製作者】DestroyerI滅世I   ")
        about.setStandardButtons(QMessageBox.Ok)
        about.setWindowTitle(QCoreApplication.translate("about", u"【提醒】此程式完全免費！", None))
        about.setStyleSheet(u"font: 75 15pt NSimSun")
        about.setWindowIcon(QIcon("icon/srcds.png"))
        about = about.exec()

        self.ui.tabWidget.currentChanged.connect(self.tabWidget)

        self.ui.steam_location_cdef.currentIndexChanged.connect(self.steam_location_cdef)
        self.ui.steam_location_full.textChanged.connect(self.steam_location_full)
        self.ui.steam_location_find.clicked.connect(self.steam_location_find)

        self.ui.workshop_add.clicked.connect(self.workshop_add)
        self.ui.workshop_remove.clicked.connect(self.workshop_remove)

        self.ui.login_token_web.clicked.connect(self.login_token_web)

        self.ui.select_server_choose.currentIndexChanged.connect(self.select_server_choose)
        self.ui.select_server_open.clicked.connect(self.select_server_open)

        self.ui.custom_option_choose.currentIndexChanged.connect(self.custom_option_choose)
        self.ui.custom_option_modify_choose.currentIndexChanged.connect(self.custom_option_modify_choose)
        self.ui.custom_modify_click.clicked.connect(self.custom_modify_click)
        self.ui.custom_all_default.clicked.connect(self.custom_all_default)
        self.ui.custom_onlyone_default.clicked.connect(self.custom_onlyone_default)

        #【讀取紀錄】
        if os.path.exists(r"./record") == False:
            os.mkdir(r"./record")
            with open(r"./record/uds.record", "w", encoding="UTF-8") as f:
                f.write("")
        else:
            if os.path.exists(r"./record/uds.record") == False:
                with open(r"./record/uds.record", "w", encoding="UTF-8") as f:
                    f.write("")
            else:
                with open(r"./record/uds.record", "r", encoding="UTF-8") as f:
                    for line in f.readlines():
                        if line.split()[0] == "cdef":
                            self.ui.steam_location_cdef.setCurrentText(line.split()[1])
                        if line.split()[0] == "location":
                            self.ui.steam_location_full.setText(line.split()[1])

    def tabWidget(self):
        if self.ui.select_server_choose.currentText() == "無":
            if self.ui.tabWidget.currentIndex() > 0:
                self.ui.tabWidget.setCurrentIndex(0)
                pass
        elif self.ui.select_server_choose.currentText() == "新建伺服器":
            pass

    def steam_location_cdef(self):
        if "U3DS" in self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text()\
        and os.path.exists(self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text()):
            self.ui.select_server_choose.clear()
            self.ui.select_server_choose.addItem("無")
            self.ui.select_server_choose.addItem("新建伺服器")
            for line in os.listdir(self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text() + r"/Servers/"):
                self.ui.select_server_choose.addItem(line)
        else:
            self.ui.select_server_choose.clear()
            self.ui.select_server_choose.addItem("無")
            self.ui.select_server_choose.addItem("新建伺服器")

    def steam_location_full(self):
        if "U3DS" in self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text()\
        and os.path.exists(self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text()):
            self.ui.select_server_choose.clear()
            self.ui.select_server_choose.addItem("無")
            self.ui.select_server_choose.addItem("新建伺服器")
            for line in os.listdir(self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text() + r"/Servers/"):
                self.ui.select_server_choose.addItem(line)
        else:
            self.ui.select_server_choose.clear()
            self.ui.select_server_choose.addItem("無")
            self.ui.select_server_choose.addItem("新建伺服器")

    def steam_location_find(self):
        folder_path = QFileDialog.getExistingDirectory(self, '選擇 Steam U3DS 的資料夾路徑', '/')
        errormsg = ""
        if folder_path and "U3DS" in folder_path:
            self.ui.steam_location_full.setText(folder_path.split()[0][3:].replace('/', '\\'))
            self.ui.steam_location_cdef.setCurrentText(folder_path.split()[0][0:3].replace('/', '\\'))
        else:
            errormsg = "無效的路徑選擇"
        if errormsg != "":
            error = QMessageBox()
            error.setText("【錯誤】" + errormsg + "！   ")
            error.setWindowIcon(QIcon("./icon/unturned.png"))
            error.setStyleSheet(u"font: 75 15pt NSimSun")
            error.setStandardButtons(QMessageBox.Ok)
            error.setWindowTitle(QCoreApplication.translate("close", u"ERROR", None))
            error = error.exec()
            

    def login_token_web(self):
        webbrowser.open("https://steamcommunity.com/dev/managegameservers")

    def workshop_add(self):
        errormsg = ""
        if self.ui.workshop_input.text().isdigit():
            if self.ui.workshop_choose.findText(self.ui.workshop_input.text()) == -1:
                self.ui.workshop_choose.addItem(self.ui.workshop_input.text())
                self.ui.workshop_choose.setCurrentIndex(len(self.ui.workshop_choose) - 1)
                self.ui.workshop_input.clear()
            else:
                errormsg = "重複的添加項目"
        else:
            errormsg = "無效的工作坊項目"

        if errormsg != "":
            error = QMessageBox()
            error.setText("【錯誤】" + errormsg + "！   ")
            error.setWindowIcon(QIcon("./icon/unturned.png"))
            error.setStyleSheet(u"font: 75 15pt NSimSun")
            error.setStandardButtons(QMessageBox.Ok)
            error.setWindowTitle(QCoreApplication.translate("close", u"ERROR", None))
            error = error.exec()
    
    def workshop_remove(self):
        self.ui.workshop_choose.removeItem(self.ui.workshop_choose.currentIndex())

    def select_server_choose(self):
        if self.ui.select_server_choose.currentIndex() == 1:
            self.ui.file_name_input.setText("")
            self.ui.server_name_input.setText("")
            self.ui.map_input.setText("")
            self.ui.welcome_input.setText("")
            self.ui.perspective_choose.setCurrentIndex(0)
            self.ui.difficulty_choose.setCurrentIndex(1)
            self.ui.mode_choose.setCurrentIndex(0)
            self.ui.port_input.setText("")
            self.ui.maxplayers_choose.setCurrentIndex(11)
            self.ui.password_input.setText("")
            self.ui.workshop_input.setText("")
            self.ui.workshop_choose.clear()
            self.ui.anti_cheat_vac.setChecked(True)
            self.ui.anti_cheat_battleye.setChecked(True)
            self.ui.server_subtitle_input.setText("")
            self.ui.list_server_subtitle_input.setText("")
            self.ui.server_fulldesc_input.setText("")
            self.ui.custom_difficulty_choose.setCurrentIndex(1)
            self.ui.custom_option_choose.setCurrentIndex(0)
            self.ui.custom_option_modify_choose.setCurrentIndex(0)
            self.ui.custom_option_value.setText("")
        if self.ui.select_server_choose.currentIndex() != 0\
        and self.ui.select_server_choose.currentIndex() != 1:
            self.index_to_dif = {
                0: "Easy",
                1: "Normal",
                2: "Hard"
            }
            if self.ui.custom_difficulty_choose.currentIndex() > 0:
                self.difficulty = self.index_to_dif[self.ui.custom_difficulty_choose.currentIndex()]

            self.index_to_coc = {
                0: "Items",
                1: "Vehicles",
                2: "Zombies",
                3: "Animals",
                4: "Barricades",
                5: "Structures",
                6: "Players",
                7: "Objects",
                8: "Events",
                9: "Gameplay"
            }
            self.coc = self.index_to_coc[self.ui.custom_option_choose.currentIndex()]
            self.selcht = {
                "Spawn_Chance"                           : "重新生成機率 (%)",
                "Despawn_Dropped_Time"                   : "掉落消失時間",
                "Despawn_Natural_Time"                   : "物品自然消失時間",
                "Respawn_Time"                           : "重新生成時間",
                "Quality_Full_Chance"                    : "質量 100% 機率 (%)",
                "Quality_Multiplier"                     : "質量配置 (%)",
                "Gun_Bullets_Full_Chance"                : "子彈 100% 機率 (%)",
                "Gun_Bullets_Multiplier"                 : "子彈倍數 (%)",
                "Magazine_Bullets_Full_Chance"           : "彈匣 100% 機率 (%)",
                "Magazine_Bullets_Multiplier"            : "彈匣倍數 (%)",
                "Crate_Bullets_Full_Chance"              : "彈藥箱 100% 機率 (%)",
                "Crate_Bullets_Multiplier"               : "彈藥箱倍數 (%)",
                "Has_Durability"                         : "是否具有耐久度",
                "Decay_Time"                             : "自然消失時間",
                "Decay_Damage_Per_Second"                : "每秒衰減傷害",
                "Has_Battery_Chance"                     : "擁有電池機率 (%)",
                "Min_Battery_Charge"                     : "最小電池電量 (%)",
                "Max_Battery_Charge"                     : "最大電池電量 (%)",
                "Has_Tire_Chance"                        : "擁有輪胎機率 (%)",
                "Respawn_Time"                           : "重新生成時間",
                "Unlocked_After_Seconds_In_Safezone"     : "安全區自動解鎖時間",
                "Armor_Multiplier"                       : "裝甲抗性 (%)",
                "Child_Explosion_Armor_Multiplier"       : "爆破物抗性 (%)",
                "Gun_Lowcal_Damage_Multiplier"           : "低數值彈藥抗性 (%)",
                "Gun_Highcal_Damage_Multiplier"          : "高數值彈藥抗性 (%)",
                "Melee_Damage_Multiplier"                : "近戰抗性 (%)",
                "Melee_Repair_Multiplier"                : "",
                "Max_Instances_Tiny"                     : "",
                "Max_Instances_Small"                    : "",
                "Max_Instances_Medium"                   : "",
                "Max_Instances_Large"                    : "",
                "Max_Instances_Insane"                   : "",
                "Spawn_Chance"                           : "重新生成機率 (%)",
                "Loot_Chance"                            : "物品掉落機率 (%)",
                "Crawler_Chance"                         : "殭屍狗生成機率 (%)",
                "Sprinter_Chance"                        : "爬行殭屍生成機率 (%)",
                "Flanker_Chance"                         : "隱身殭屍生成機率 (%)",
                "Burner_Chance"                          : "火焰殭屍生成機率 (%)",
                "Acid_Chance"                            : "噴液殭屍生成機率 (%)",
                "Boss_Electric_Chance"                   : "雷電王殭屍生成機率 (%)",
                "Boss_Wind_Chance"                       : "颶風王殭屍生成機率 (%)",
                "Boss_Fire_Chance"                       : "炙焱王殭屍生成機率 (%)",
                "Spirit_Chance"                          : "隱身殭屍生成機率 (%)",
                "DL_Red_Volatile_Chance"                 : "",
                "DL_Blue_Volatile_Chance"                : "",
                "Boss_Elver_Stomper_Chance"              : "",
                "Boss_Kuwait_Chance"                     : "",
                "Respawn_Day_Time"                       : "白天殭屍生成時間",
                "Respawn_Night_Time"                     : "夜晚殭屍生成時間",
                "Respawn_Beacon_Time"                    : "屍潮機殭屍生成時間",
                "Quest_Boss_Respawn_Interval"            : "任務BOSS重生時間間隔",
                "Damage_Multiplier"                      : "造成傷害倍率 (%)",
                "Armor_Multiplier"                       : "防禦抗性倍率 (%)",
                "Backstab_Multiplier"                    : "對殭屍背刺傷害倍率 (%)",
                "NonHeadshot_Armor_Multiplier"           : "對殭屍非爆頭傷害倍率 (%)",
                "Beacon_Experience_Multiplier"           : "屍潮機經驗倍率 (%)",
                "Full_Moon_Experience_Multiplier"        : "滿月經驗倍率 (%)",
                "Min_Drops"                              : "最小掉落數量",
                "Max_Drops"                              : "最大掉落數量",
                "Min_Mega_Drops"                         : "特殊殭屍最小掉落數量",
                "Max_Mega_Drops"                         : "特殊殭屍最大掉落數量",
                "Min_Boss_Drops"                         : "BOSS殭屍最小掉落數量",
                "Max_Boss_Drops"                         : "BOSS殭屍最大掉落數量",
                "Slow_Movement"                          : "是否啟用慢模式",
                "Can_Stun"                               : "是否擊暈殭屍",
                "Only_Critical_Stuns"                    : "是否只持有重型武器才能擊暈",
                "Weapons_Use_Player_Damage"              : "是否只持有武器才能造成傷害",
                "Can_Target_Barricades"                  : "是否可以對障礙物造成傷害",
                "Can_Target_Structures"                  : "是否可以對建築物造成傷害",
                "Can_Target_Vehicles"                    : "是否可以對載具造成傷害",
                "Beacon_Max_Rewards"                     : "屍潮機最大獎勵",
                "Beacon_Max_Participants"                : "屍潮機最大參與玩家數",
                "Beacon_Rewards_Multiplier"              : "屍潮機獎勵倍數 (%)",
                "Respawn_Time"                           : "重新生成時間",
                "Damage_Multiplier"                      : "造成傷害倍率 (%)",
                "Armor_Multiplier"                       : "防禦抗性倍率 (%)",
                "Max_Instances_Tiny"                     : "",
                "Max_Instances_Small"                    : "",
                "Max_Instances_Medium"                   : "",
                "Max_Instances_Large"                    : "",
                "Max_Instances_Insane"                   : "",
                "Weapons_Use_Player_Damage"              : "是否只持有武器才能造成傷害",
                "Decay_Time"                             : "自然消失時間",
                "Armor_Lowtier_Multiplier"               : "低數值防禦抗性 (%)",
                "Armor_Hightier_Multiplier"              : "高數值防禦抗性 (%)",
                "Gun_Lowcal_Damage_Multiplier"           : "低數值彈藥抗性 (%)",
                "Gun_Highcal_Damage_Multiplier"          : "高數值彈藥抗性 (%)",
                "Melee_Damage_Multiplier"                : "近戰抗性 (%)",
                "Melee_Repair_Multiplier"                : "",
                "Allow_Item_Placement_On_Vehicle"        : "是否可以在載具上放置物品",
                "Allow_Trap_Placement_On_Vehicle"        : "是否可以在載具上放置陷阱",
                "Max_Item_Distance_From_Hull"            : "最大物品與船體的距離",
                "Max_Trap_Distance_From_Hull"            : "最大陷阱與船體的距離",
                "Decay_Time"                             : "自然消失時間",
                "Armor_Lowtier_Multiplier"               : "低數值防禦抗性 (%)",
                "Armor_Hightier_Multiplier"              : "高數值防禦抗性 (%)",
                "Gun_Lowcal_Damage_Multiplier"           : "低數值彈藥抗性 (%)",
                "Gun_Highcal_Damage_Multiplier"          : "高數值彈藥抗性 (%)",
                "Melee_Damage_Multiplier"                : "近戰抗性 (%)",
                "Melee_Repair_Multiplier"                : "",
                "Health_Default"                         : "預設血量",
                "Health_Regen_Min_Food"                  : "自然生命恢復最低需求飽食度",
                "Health_Regen_Min_Water"                 : "自然生命恢復最低需求水分值",
                "Health_Regen_Ticks"                     : "自然生命恢復所需時間",
                "Food_Default"                           : "預設飽食度",
                "Food_Use_Ticks"                         : "飽食度消耗頻率",
                "Food_Damage_Ticks"                      : "飽食度歸零生命流失頻率",
                "Water_Default"                          : "預設水分值",
                "Water_Use_Ticks"                        : "水分值消耗頻率",
                "Water_Damage_Ticks"                     : "水分值歸零生命流失頻率",
                "Virus_Default"                          : "預設健康值",
                "Virus_Infect"                           : "開始自然下降健康值數",
                "Virus_Use_Ticks"                        : "健康值消耗頻率",
                "Virus_Damage_Ticks"                     : "健康值歸零生命流失頻率",
                "Leg_Regen_Ticks"                        : "自然恢復骨折所需時間",
                "Bleed_Damage_Ticks"                     : "失血狀態生命流失頻率",
                "Bleed_Regen_Ticks"                      : "自動癒合失血所需時間",
                "Armor_Multiplier"                       : "抗性倍數 (%)",
                "Experience_Multiplier"                  : "給予玩家經驗倍率 (%)",
                "Detect_Radius_Multiplier"               : "視野半徑 (%)",
                "Ray_Aggressor_Distance"                 : "直接攻擊目標距離拋物線 (%)",
                "Lose_Skills_PvP"                        : "在PVP模式中遺失經驗 (%)",
                "Lose_Skills_PvE"                        : "在PVE模式中遺失經驗 (%)",
                "Lose_Items_PvP"                         : "在PVP模式中遺失物品 (%)",
                "Lose_Items_PvE"                         : "在PVE模式中遺失物品 (%)",
                "Lose_Clothes_PvP"                       : "在PVP模式中遺失衣物",
                "Lose_Clothes_PvE"                       : "在PVE模式中遺失衣物",
                "Lose_Weapons_PvP"                       : "在PVP模式中遺失武器",
                "Lose_Weapons_PvE"                       : "在PVE模式中遺失武器",
                "Can_Hurt_Legs"                          : "摔落是否造成傷害",
                "Can_Break_Legs"                         : "摔落是否骨折",
                "Can_Fix_Legs"                           : "是否治療骨折",
                "Can_Start_Bleeding"                     : "是否可以造成失血",
                "Can_Stop_Bleeding"                      : "是否治療失血",
                "Spawn_With_Max_Skills"                  : "重生後是否點滿技能",
                "Spawn_With_Stamina_Skills"              : "重生後是否具有耐力技能",
                "Allow_Instakill_Headshots"              : "是否允許重型狙擊槍一槍暴頭死亡",
                "Allow_Per_Character_Saves"              : "",
                "Binary_State_Reset_Multiplier"          : "物體二進制狀態時長 (%)",
                "Fuel_Reset_Multiplier"                  : "燃料重生時長 (%)",
                "Water_Reset_Multiplier"                 : "水資源重生時長 (%)",
                "Resource_Reset_Multiplier"              : "資源重生時長 (%)",
                "Resource_Drops_Multiplier"              : "物品掉落時長 (%)",
                "Rubble_Reset_Multiplier"                : "碎片資源重生時長 (%)",
                "Allow_Holiday_Drops"                    : "允許空間丟失 (%)",
                "Items_Obstruct_Tree_Respawns"           : "允許物品、障礙物、樹重新生成",
                "Rain_Frequency_Min"                     : "降雨最低頻率 (時)",
                "Rain_Frequency_Max"                     : "降雨最高頻率 (時)",
                "Rain_Duration_Min"                      : "降雨最短持續時間 (時)",
                "Rain_Duration_Max"                      : "降雨最長持續時間 (時)",
                "Snow_Frequency_Min"                     : "降雪最低頻率 (時)",
                "Snow_Frequency_Max"                     : "降雪最高頻率 (時)",
                "Snow_Duration_Min"                      : "降雪最短持續時間 (時)",
                "Snow_Duration_Max"                      : "降雪最長持續時間 (時)",
                "Weather_Frequency_Multiplier"           : "",
                "Weather_Duration_Multiplier"            : "",
                "Airdrop_Frequency_Min"                  : "空投補給最低頻率 (時)",
                "Airdrop_Frequency_Max"                  : "空投補給最高頻率 (時)",
                "Airdrop_Speed"                          : "空投速度",
                "Airdrop_Force"                          : "空投範圍大小",
                "Arena_Min_Players"                      : "競技場模式最小人數",
                "Arena_Compactor_Damage"                 : "競技場模式縮圈傷害",
                "Arena_Compactor_Extra_Damage_Per_Second": "",
                "Arena_Clear_Timer"                      : "競技場模式清場時間",
                "Arena_Finale_Timer"                     : "競技場模式決賽時間",
                "Arena_Restart_Timer"                    : "競技場模式重置時間",
                "Arena_Compactor_Delay_Timer"            : "競技場模式縮圈延遲",
                "Arena_Compactor_Pause_Timer"            : "競技場模式縮圈停頓",
                "Use_Airdrops"                           : "允許空投",
                "Arena_Use_Compactor_Pause"              : "競技場模式是否開放縮圈停頓",
                "Arena_Compactor_Speed_Tiny"             : "",
                "Arena_Compactor_Speed_Small"            : "",
                "Arena_Compactor_Speed_Medium"           : "",
                "Arena_Compactor_Speed_Large"            : "",
                "Arena_Compactor_Speed_Insane"           : "",
                "Arena_Compactor_Shrink_Factor"          : "",
                "Repair_Level_Max"                       : "最大維修等擊",
                "Hitmarkers"                             : "是否啟用命中目標顯示標記",
                "Crosshair"                              : "是否啟用準新",
                "Ballistics"                             : "是否啟用彈道",
                "Chart"                                  : "是否啟用地圖",
                "Satellite"                              : "是否啟用衛星定位系統",
                "Compass"                                : "是否啟用羅盤",
                "Group_Map"                              : "是否啟用群組地圖",
                "Group_HUD"                              : "是否啟用群組HUD",
                "Group_Player_List"                      : "是否啟用群組玩家清單",
                "Allow_Static_Groups"                    : "是否啟用固定群組",
                "Allow_Dynamic_Groups"                   : "是否啟用換群組功能",
                "Allow_Lobby_Groups"                     : "是否啟用大廳群組",
                "Allow_Shoulder_Camera"                  : "是否啟用第三人稱",
                "Can_Suicide"                            : "是否啟用自殺",
                "Friendly_Fire"                          : "是否啟用友方傷害",
                "Bypass_Buildable_Mobility"              : "",
                "Allow_Holidays"                         : "是否啟用特殊節日",
                "Timer_Exit"                             : "退出伺服器等待時長",
                "Timer_Respawn"                          : "重生所需時長",
                "Timer_Home"                             : "重生至家裡所需時長",
                "Timer_Leave_Group"                      : "離開群組等待時間",
                "Max_Group_Members"                      : "最大群組成員數量",
                "Explosion_Launch_Speed_Multiplier"      : "",
                "AirStrafing_Acceleration_Multiplier"    : "",
                "AirStrafing_Deceleration_Multiplier"    : "",
                "ThirdPerson_RecoilMultiplier"           : "",
                "ThirdPerson_SpreadMultiplier"           : ""
            }
            if os.path.exists(self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text() + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Server\\Commands.dat"):
                with open(self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text() + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Server\\Commands.dat", "r", encoding="UTF-8") as f:
                    self.ui.file_name_input.setText(self.ui.select_server_choose.currentText())
                    for line in f.readlines():
                        if line.split()[0] == "Name":
                            self.ui.server_name_input.setText(line[len("Name"):].strip())
                        if line.split()[0] == "Map":
                            self.ui.map_input.setText(line[len("Map"):].strip())
                        if line.split()[0] == "Welcome":
                            self.ui.welcome_input.setText(line[len("Welcome"):].strip())
                        if line.split()[0] == "Perspective":
                            if line.split()[1] == "Both":
                                self.ui.perspective_choose.setCurrentIndex(0)
                        if line.split()[0] == "Mode":
                            if line.split()[1].lower() == "easy":
                                self.ui.difficulty_choose.setCurrentIndex(0)
                            if line.split()[1].lower() == "normal":
                                self.ui.difficulty_choose.setCurrentIndex(1)
                            if line.split()[1].lower() == "hard":
                                self.ui.difficulty_choose.setCurrentIndex(2)
                            if line.split()[1].lower() == "custom":
                                self.ui.difficulty_choose.setCurrentIndex(3)
                        if line.split()[0] == "PVE":
                            self.ui.mode_choose.setCurrentIndex(0)
                        if line.split()[0] == "PVP":
                            self.ui.mode_choose.setCurrentIndex(1)
                        if line.split()[0] == "Port":
                            self.ui.port_input.setText(line.split()[1])
                        if line.split()[0] == "MaxPlayers":
                            self.ui.maxplayers_choose.setCurrentText(line.split()[1])
                        if line.split()[0] == "Password":
                            self.ui.password_input.setText(line.split()[1])
            if os.path.exists(self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text() + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Config.json"):
                with open(self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text() + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Config.json", "r", encoding="UTF-8") as f:
                    self.configdata = json.load(f)
                    self.ui.login_token_input.setText(self.configdata["Browser"]["Login_Token"])
                    self.ui.anti_cheat_vac.setChecked(self.configdata["Server"]["VAC_Secure"])
                    self.ui.anti_cheat_battleye.setChecked(self.configdata["Server"]["BattlEye_Secure"])
                    self.ui.server_subtitle_input.setText(self.configdata["Browser"]["Desc_Hint"])
                    self.ui.list_server_subtitle_input.setText(self.configdata["Browser"]["Desc_Server_List"])
                    self.ui.server_fulldesc_input.setText(self.configdata["Browser"]["Desc_Full"])
                    difficulty = ""
                    if self.ui.custom_difficulty_choose.currentIndex() == 0:
                        difficulty = "Easy"
                    elif self.ui.custom_difficulty_choose.currentIndex() == 1:
                        difficulty = "Normal"
                    elif self.ui.custom_difficulty_choose.currentIndex() == 2:
                        difficulty = "Hard"
                    self.ui.custom_option_modify_choose.clear()
                    for option in self.configdata[difficulty]:
                        for select in self.configdata[difficulty][option]:
                            if option == "Items":
                                if self.selcht[select] == "":
                                    self.ui.custom_option_modify_choose.addItem(select)
                                else:
                                    self.ui.custom_option_modify_choose.addItem(self.selcht[select])
                            if option == "Vehicles":
                                pass
                            if option == "Zombies":
                                pass
                            if option == "Animals":
                                pass
                            if option == "Barricades":
                                pass
                            if option == "Structures":
                                pass
                            if option == "Players":
                                pass
                            if option == "Objects":
                                pass
                            if option == "Events":
                                pass
                            if option == "Gameplay":
                                pass

            if os.path.exists(self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text() + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\WorkshopDownloadConfig.json"):
                with open(self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text() + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\WorkshopDownloadConfig.json", "r", encoding="UTF-8") as f:
                    self.workshopconfigdata = json.load(f)
                    self.ui.workshop_choose.clear()
                    for id in self.workshopconfigdata.get("File_IDs"):
                        self.ui.workshop_choose.addItem(str(id))

    def custom_option_choose(self):
        self.ui.custom_option_modify_choose.clear()
        self.ui.custom_option_modify_choose.setCurrentIndex(0)
        self.difficulty = self.index_to_dif[self.ui.custom_difficulty_choose.currentIndex()]
        self.coc = self.index_to_coc[self.ui.custom_option_choose.currentIndex()]
        for select in self.configdata[self.difficulty][self.coc]:
            if self.selcht[select] == "":
                self.ui.custom_option_modify_choose.addItem(select)
            else:
                self.ui.custom_option_modify_choose.addItem(self.selcht[select])

    def custom_option_modify_choose(self):
        self.file_path = self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text()

        self.difficulty = self.index_to_dif[self.ui.custom_difficulty_choose.currentIndex()]
        self.coc = self.index_to_coc[self.ui.custom_option_choose.currentIndex()]
        
        if self.ui.custom_option_modify_choose.currentText() != "":
            reverse_selcht = {v: k for k, v in self.selcht.items()}
            if reverse_selcht.get(self.ui.custom_option_modify_choose.currentText()) != None:
                if self.configdata[self.difficulty][self.coc][reverse_selcht.get(self.ui.custom_option_modify_choose.currentText())]:
                    self.ui.custom_option_value.setText(str(self.configdata[self.difficulty][self.coc][reverse_selcht.get(self.ui.custom_option_modify_choose.currentText())]))
            else:
                if self.configdata[self.difficulty][self.coc][self.ui.custom_option_modify_choose.currentText()]:
                    self.ui.custom_option_value.setText(str(self.configdata[self.difficulty][self.coc][self.ui.custom_option_modify_choose.currentText()]))

    def custom_modify_click(self):
        errormsg = ""
        self.file_path = self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text()

        reverse_selcht = {v: k for k, v in self.selcht.items()}

        modifychoosetext = ""
        if self.ui.custom_option_value.text() != "":
            if reverse_selcht.get(self.ui.custom_option_modify_choose.currentText()) != None:
                if self.configdata[self.difficulty][self.coc][reverse_selcht.get(self.ui.custom_option_modify_choose.currentText())]:
                    modifychoosetext = reverse_selcht.get(self.ui.custom_option_modify_choose.currentText())
            else:
                if self.configdata[self.difficulty][self.coc][self.ui.custom_option_modify_choose.currentText()]:
                    modifychoosetext = self.ui.custom_option_modify_choose.currentText()

        if self.ui.custom_option_value.text() != "":
            if self.ui.custom_option_value.text() == "True":
                self.configdata[self.difficulty][self.coc][modifychoosetext] = True
            elif self.ui.custom_option_value.text() == "False":
                self.configdata[self.difficulty][self.coc][modifychoosetext] = False
            try:
                self.configdata[self.difficulty][self.coc][modifychoosetext] = float(self.ui.custom_option_value.text())
            except ValueError:
                errormsg = "無效的數值"
            with open(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Config.json", "w", encoding="utf-8") as f:
                json.dump(self.configdata, f, indent = 2)
        else:
            errormsg = "無效的數值"

        if errormsg != "":
            error = QMessageBox()
            error.setText("【錯誤】" + errormsg + "！   ")
            error.setWindowIcon(QIcon("./icon/unturned.png"))
            error.setStyleSheet(u"font: 75 15pt NSimSun")
            error.setStandardButtons(QMessageBox.Ok)
            error.setWindowTitle(QCoreApplication.translate("close", u"ERROR", None))
            error = error.exec()
        

    def custom_all_default(self):
        self.file_path = self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text()
        with open("./default_file/Config.json", "r", encoding="UTF-8") as f:
            self.defconfigdata = json.load(f)
        self.ui.custom_option_modify_choose.clear()
        self.ui.custom_option_modify_choose.setCurrentIndex(0)
        for i in self.configdata[self.difficulty][self.coc]:
            self.configdata[self.difficulty][self.coc][i] = self.defconfigdata[self.difficulty][self.coc][i]
        with open(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Config.json", "w", encoding="utf-8") as f:
            json.dump(self.configdata, f, indent = 2)
        self.ui.custom_option_modify_choose.clear()
        self.ui.custom_option_modify_choose.setCurrentIndex(0)
        for select in self.configdata[self.difficulty][self.coc]:
            if self.selcht[select] == "":
                self.ui.custom_option_modify_choose.addItem(select)
            else:
                self.ui.custom_option_modify_choose.addItem(self.selcht[select])


    def custom_onlyone_default(self):
        self.file_path = self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text()

        reverse_selcht = {v: k for k, v in self.selcht.items()}

        modifychoosetext = ""
        if reverse_selcht.get(self.ui.custom_option_modify_choose.currentText()) != None:
            if self.configdata[self.difficulty][self.coc][reverse_selcht.get(self.ui.custom_option_modify_choose.currentText())]:
                modifychoosetext = reverse_selcht.get(self.ui.custom_option_modify_choose.currentText())
        else:
            if self.configdata[self.difficulty][self.coc][self.ui.custom_option_modify_choose.currentText()]:
                modifychoosetext = self.ui.custom_option_modify_choose.currentText()

        with open("./default_file/Config.json", "r", encoding="UTF-8") as f:
            self.defconfigdata = json.load(f)
        self.configdata[self.difficulty][self.coc][modifychoosetext] = self.defconfigdata[self.difficulty][self.coc][modifychoosetext]
        self.ui.custom_option_value.setText(str(self.defconfigdata[self.difficulty][self.coc][modifychoosetext]))
        with open(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Config.json", "w", encoding="utf-8") as f:
            json.dump(self.configdata, f, indent = 2)

    def select_server_open(self):
        errormsg = ""
        self.file_path = self.ui.steam_location_cdef.currentText() + self.ui.steam_location_full.text()
        if not os.path.exists(self.file_path):
            errormsg = "無效的 Steam 檔案路徑"
        elif self.ui.select_server_choose.currentText() == "無":
            errormsg = "未選擇檔案"
        elif self.ui.login_token_input.text() == "":
            errormsg = "Login Token 未填"
        elif self.ui.map_input.text() == "":
            errormsg = "無效的地圖名稱"
        else:
            today = date.today()
            year = today.year % 100
            month = today.month
            day = today.day
            result = year * 10000 + month * 100 + day
            if self.ui.file_name_input.text() == "":
                self.ui.file_name_input.setText("map_" + self.ui.map_input.text() + "_" + str(result))
            if self.ui.server_name_input.text() == "":
                self.ui.server_name_input.setText("my new " + self.ui.map_input.text() + " server (" + str(result) + ")")
            if self.ui.welcome_input.text() == "":
                self.ui.welcome_input.setText("welcome join to my server!")
            if self.ui.port_input.text() == "":
                self.ui.port_input.setText("27015")
            if self.ui.select_server_choose.currentText() == "新建伺服器":
                repeat = False
                ssc_val = [self.ui.select_server_choose.itemText(i) for i in range(self.ui.select_server_choose.count())]
                for value in ssc_val:
                    if value == self.ui.file_name_input.text():
                        repeat = True
                if repeat:
                    errormsg = "重複的檔案名稱"
                else:
                    self.ui.select_server_choose.addItem(self.ui.file_name_input.text())
                    self.ui.select_server_choose.setCurrentIndex(len(self.ui.select_server_choose) - 1)
                    os.mkdir(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText())
                    os.mkdir(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Server")
                    shutil.copy("./default_file/Config.json", self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText())
                    shutil.copy("./default_file/WorkshopDownloadConfig.json", self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText())
                    self.configdata["Browser"]["Login_Token"] = self.ui.login_token_input.text()
                    self.configdata["Server"]["VAC_Secure"] = self.ui.anti_cheat_vac.isChecked()
                    self.configdata["Server"]["BattlEye_Secure"] = self.ui.anti_cheat_vac.isChecked()
                    self.configdata["Server"]["Desc_Hint"] = self.ui.server_subtitle_input.text()
                    self.configdata["Server"]["Desc_Full"] = self.ui.server_fulldesc_input.toPlainText()
                    self.configdata["Server"]["Desc_Server_List"] = self.ui.list_server_subtitle_input.text()
                    with open(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Config.json", "w", encoding="utf-8") as f:
                        json.dump(self.configdata, f, indent = 2)
                    combo_box_values = [self.ui.workshop_choose.itemText(i) for i in range(self.ui.workshop_choose.count())]
                    self.workshopconfigdata["File_IDs"] = []
                    for value in combo_box_values:
                        self.workshopconfigdata["File_IDs"].append(value)
                    with open(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\WorkshopDownloadConfig.json", "w", encoding="utf-8") as f:
                        json.dump(self.workshopconfigdata, f, indent = 2)
                    with open(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Server\\Commands.dat", "w", encoding="utf-8") as f:
                        perspective = ""
                        difficulty = ""
                        if self.ui.perspective_choose.currentIndex() == 0:
                            perspective = "Both"
                        if self.ui.difficulty_choose.currentIndex() == 0:
                            difficulty = "Easy"
                        elif self.ui.difficulty_choose.currentIndex() == 1:
                            difficulty = "Normal"
                        elif self.ui.difficulty_choose.currentIndex() == 2:
                            difficulty = "Hard"
                        
                        write = (
                            "Cycle 2400" +
                            "\nTimeout 1500" +
                            "\nName " + self.ui.server_name_input.text() +
                            "\nPerspective " + perspective +
                            "\nMaxPlayers " + self.ui.maxplayers_choose.currentText() +
                            "\nMap " + self.ui.map_input.text() +
                            "\nMode " + difficulty +
                            "\n" + self.ui.mode_choose.currentText() +
                            "\nPort " + self.ui.port_input.text() +
                            "\nWelcome " + self.ui.welcome_input.text()
                        )
                            
                        if self.ui.password_input.text() != "":
                            write = write + "\nPassword " + self.ui.password_input.text()

                        if self.ui.cheat_allow_check.isChecked():
                            write = write + "\nCheats enable"

                        f.write(write)

                        with open(self.file_path + "\\serverhelper.bat", "w", encoding="utf-8") as f:
                            f.write(
                                "\n@echo off" +
                                '\nstart "" "%~dp0Unturned.exe" -batchmode -nographics %*' +
                                "\nexit"
                            )
                        with open(self.file_path + "\\serverstarter.bat", "w", encoding="utf-8") as f:
                            f.write(
                                "\n@echo off" +
                                '\nstart "" "%~dp0serverhelper.bat" -OpenModAutoUpdate -port/' + self.ui.port_input.text() + " +secureserver/" + self.ui.file_name_input.text() +
                                "\nexit"
                            )
                        os.system(self.file_path + "\\serverstarter.bat")

                        with open("./record/uds.record", "w", encoding="utf-8") as f:
                            f.write(
                                "cdef " + self.ui.steam_location_cdef.currentText() +
                                "\nlocation " + self.ui.steam_location_full.text()
                            )
            else:
                self.configdata["Browser"]["Login_Token"] = self.ui.login_token_input.text()
                self.configdata["Server"]["VAC_Secure"] = self.ui.anti_cheat_vac.isChecked()
                self.configdata["Server"]["BattlEye_Secure"] = self.ui.anti_cheat_vac.isChecked()
                self.configdata["Server"]["Desc_Hint"] = self.ui.server_subtitle_input.text()
                self.configdata["Server"]["Desc_Full"] = self.ui.server_fulldesc_input.toPlainText()
                self.configdata["Server"]["Desc_Server_List"] = self.ui.list_server_subtitle_input.text()
                with open(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Config.json", "w", encoding="utf-8") as f:
                    json.dump(self.configdata, f, indent = 2)
                combo_box_values = [self.ui.workshop_choose.itemText(i) for i in range(self.ui.workshop_choose.count())]
                self.workshopconfigdata["File_IDs"] = []
                for value in combo_box_values:
                    self.workshopconfigdata["File_IDs"].append(value)
                with open(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\WorkshopDownloadConfig.json", "w", encoding="utf-8") as f:
                    json.dump(self.workshopconfigdata, f, indent = 2)
                with open(self.file_path + "\\Servers\\" + self.ui.select_server_choose.currentText() + "\\Server\\Commands.dat", "w", encoding="utf-8") as f:
                    perspective = ""
                    difficulty = ""
                    if self.ui.perspective_choose.currentIndex() == 0:
                        perspective = "Both"
                    if self.ui.difficulty_choose.currentIndex() == 0:
                        difficulty = "Easy"
                    elif self.ui.difficulty_choose.currentIndex() == 1:
                        difficulty = "Normal"
                    elif self.ui.difficulty_choose.currentIndex() == 2:
                        difficulty = "Hard"
                    elif self.ui.difficulty_choose.currentIndex() == 3:
                        difficulty = "Custom"

                    write = (
                        "Cycle 2400" +
                        "\nTimeout 1500" +
                        "\nName " + self.ui.server_name_input.text() +
                        "\nPerspective " + perspective +
                        "\nMaxPlayers " + self.ui.maxplayers_choose.currentText() +
                        "\nMap " + self.ui.map_input.text() +
                        "\nMode " + difficulty +
                        "\n" + self.ui.mode_choose.currentText() +
                        "\nPort " + self.ui.port_input.text() +
                        "\nWelcome " + self.ui.welcome_input.text()
                    )
                            
                    if self.ui.password_input.text() != "":
                        write = write + "\nPassword " + self.ui.password_input.text()

                    if self.ui.cheat_allow_check.isChecked():
                        write = write + "\nCheats enable"

                    f.write(write)

                    with open(self.file_path + "\\serverhelper.bat", "w", encoding="utf-8") as f:
                        f.write(
                            "\n@echo off" +
                            '\nstart "" "%~dp0Unturned.exe" -batchmode -nographics %*' +
                            "\nexit"
                        )
                    with open(self.file_path + "\\serverstarter.bat", "w", encoding="utf-8") as f:
                        f.write(
                            "\n@echo off" +
                            '\nstart "" "%~dp0serverhelper.bat" -OpenModAutoUpdate -port/' + self.ui.port_input.text() + " +secureserver/" + self.ui.file_name_input.text() +
                            "\nexit"
                        )
                    os.system(self.file_path + "\\serverstarter.bat")

                    #exe_path = self.file_path + "\\Unturned.exe"
                    #parameters = "-batchmode -nographics -port/" + self.ui.port_input.text() + "+secureserver/" + self.ui.file_name_input.text()

                    with open("./record/uds.record", "w", encoding="utf-8") as f:
                        f.write(
                            "cdef " + self.ui.steam_location_cdef.currentText() +
                            "\nlocation " + self.ui.steam_location_full.text()
                        )

        if errormsg != "":
            error = QMessageBox()
            error.setText("【錯誤】" + errormsg + "！   ")
            error.setWindowIcon(QIcon("./icon/unturned.png"))
            error.setStyleSheet(u"font: 75 15pt NSimSun")
            error.setStandardButtons(QMessageBox.Ok)
            error.setWindowTitle(QCoreApplication.translate("close", u"ERROR", None))
            error = error.exec()

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("是否要儲存本次設定?")
        close.setWindowIcon(QIcon("icon/srcds.png"))
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close.setWindowTitle(QCoreApplication.translate("closewindow", u"關閉", None))
        close.setStyleSheet(u"font: 75 15pt NSimSun")
        close = close.exec()
        if close == QMessageBox.Yes:
            with open("./record/uds.record", "w", encoding="utf-8") as f:
                f.write(
                    "cdef " + self.ui.steam_location_cdef.currentText() +
                    "\nlocation " + self.ui.steam_location_full.text()
                )
        else:
            event.ignore()
            sys.exit(app.exec_())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())