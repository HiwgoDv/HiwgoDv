import pygame
import math
import random
import os
import sys

# เริ่มต้น Pygame และตรวจสอบการใช้งาน
pygame.init()
if pygame.get_init():
    print("Pygame เริ่มต้นสำเร็จ")
else:
    print("เกิดข้อผิดพลาดในการเริ่มต้น Pygame")
    sys.exit(1)

# ค่าคงที่ของเกม
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (180, 0, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (205, 133, 63)
SKY_BLUE = (135, 206, 235)
GRASS_GREEN = (34, 139, 34)
GOLDEN = (255, 215, 0)
CLOUD_COLOR = (240, 240, 240)
GRAVITY = 10.0  # แรงโน้มถ่วง 10 m/s²

# การตั้งค่าหน้าจอ
try:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Archery Game")
    print("Screen created successfully, size:", WIDTH, "x", HEIGHT)
except pygame.error as e:
    print(f"เกิดข้อผิดพลาดในการสร้างหน้าจอ: {e}")
    pygame.quit()
    sys.exit(1)
clock = pygame.time.Clock()

# วาดลูกธนูแทนการโหลดรูปภาพ
def create_arrow_surface(width=40, height=10):
    arrow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    # วาดลำตัวลูกธนู
    pygame.draw.rect(arrow_surface, BROWN, (0, height//4, width*3//4, height//2))
    # วาดหัวลูกธนู
    pygame.draw.polygon(arrow_surface, DARK_RED, [(width*3//4, 0), (width, height//2), (width*3//4, height)])
    # วาดขนลูกธนู
    pygame.draw.rect(arrow_surface, LIGHT_BROWN, (0, 0, width//10, height))
    return arrow_surface

arrow_img = create_arrow_surface(40, 10)

# การตั้งค่าของเป้าหมาย
target_radius = 40
target_rings = [(target_radius, RED), 
               (target_radius * 0.8, WHITE), 
               (target_radius * 0.6, RED), 
               (target_radius * 0.4, WHITE), 
               (target_radius * 0.2, GOLDEN)]

# ฟอนต์
font = pygame.font.SysFont('Arial', 24)

def draw_background():
    """วาดพื้นหลังเกมด้วยท้องฟ้า ภูเขา และหญ้า"""
    # ไล่ระดับสีท้องฟ้า
    for y in range(HEIGHT):
        # สร้างสีท้องฟ้าไล่ระดับจากสีน้ำเงินเข้มสู่สีฟ้าอ่อน
        depth = 1 - (y / HEIGHT * 0.7)
        sky_color = (int(135 * depth), int(206 * depth), int(235 * depth))
        pygame.draw.line(screen, sky_color, (0, y), (WIDTH, y))

    # ภูเขาในพื้นหลัง
    mountain_color = (100, 100, 100)
    mountain_points = [(0, HEIGHT-150), (WIDTH/4, HEIGHT-250), 
                       (WIDTH/2, HEIGHT-200), (WIDTH*3/4, HEIGHT-280), 
                       (WIDTH, HEIGHT-180), (WIDTH, HEIGHT-100), (0, HEIGHT-100)]
    pygame.draw.polygon(screen, mountain_color, mountain_points)

    # พระอาทิตย์พร้อมรังสี
    sun_x, sun_y = WIDTH - 100, 100
    # พระอาทิตย์หลัก
    pygame.draw.circle(screen, GOLDEN, (sun_x, sun_y), 40)
    # รัศมีพระอาทิตย์ - ใช้สีที่อ่อนลงตามระยะแทนการใช้ alpha
    for i, radius in enumerate(range(45, 60, 5)):
        # สีที่จางลงตามระยะ (RGB ที่ถูกต้อง)
        sun_glow_color = (255, 215, max(0, 100 - i*30))
        try:
            pygame.draw.circle(screen, sun_glow_color, (sun_x, sun_y), radius, 2)
        except pygame.error:
            print(f"ข้อผิดพลาดในการวาดรัศมีพระอาทิตย์: {sun_glow_color}")

    # วาดรังสีพระอาทิตย์
    for angle in range(0, 360, 30):
        end_x = sun_x + math.cos(math.radians(angle)) * 60
        end_y = sun_y + math.sin(math.radians(angle)) * 60
        pygame.draw.line(screen, GOLDEN, (sun_x, sun_y), (end_x, end_y), 2)

    # หญ้าพร้อมลวดลาย
    pygame.draw.rect(screen, GRASS_GREEN, (0, HEIGHT - 100, WIDTH, 100))
    # เพิ่มรายละเอียดหญ้า
    for i in range(0, WIDTH, 20):
        grass_height = random.randint(5, 15)
        pygame.draw.line(screen, (45, 160, 45), (i, HEIGHT - 100), (i, HEIGHT - 100 - grass_height), 2)

def draw_archer(x, y, angle, draw_arrow=True):
    """วาดตัวนักยิงธนูที่มีรายละเอียดมากขึ้น"""
    # คำนวณการหมุนของร่างกายนักยิงธนูตามมุม (เพื่อหันไปทิศทางเดียวกับการยิง)
    body_angle = min(max(angle, -45), 45)  # จำกัดการหมุนของร่างกายไม่ให้มากเกินไป
    
    # ลำตัว - หมุนตามมุมเล็กน้อย
    body_color = (80, 60, 40)
    body_top_x = x - 30
    body_top_y = y
    body_bottom_x = body_top_x + math.sin(math.radians(body_angle)) * 5
    body_bottom_y = y + 40
    pygame.draw.line(screen, body_color, (body_top_x, body_top_y), (body_bottom_x, body_bottom_y), 5)

    # ศีรษะ - หมุนตามร่างกายเล็กน้อย
    head_color = (210, 180, 140)
    head_x = body_top_x + math.sin(math.radians(body_angle)) * 3
    head_y = y - 10
    pygame.draw.circle(screen, head_color, (head_x, head_y), 8)

    # แขน - ปรับตามมุม
    arm_joint_x = body_top_x + math.sin(math.radians(body_angle)) * 2
    arm_joint_y = y + 10
    
    # แขนที่ถือคันธนู - ยืดออกไปตามทิศทางการยิง
    bow_arm_x = arm_joint_x + math.cos(math.radians(angle)) * 25
    bow_arm_y = arm_joint_y + math.sin(math.radians(angle)) * 10
    pygame.draw.line(screen, body_color, (arm_joint_x, arm_joint_y), (bow_arm_x, bow_arm_y), 4)
    
    # แขนที่ดึงสายธนู
    draw_arm_x = arm_joint_x - 5
    draw_arm_y = arm_joint_y + 5
    pygame.draw.line(screen, body_color, (arm_joint_x, arm_joint_y), (draw_arm_x, draw_arm_y), 4)

    # ขา
    leg_joint_x = body_bottom_x
    leg_joint_y = body_bottom_y
    left_foot_x = leg_joint_x - 5
    right_foot_x = leg_joint_x + 5
    foot_y = leg_joint_y + 15
    pygame.draw.line(screen, body_color, (leg_joint_x, leg_joint_y), (left_foot_x, foot_y), 4)
    pygame.draw.line(screen, body_color, (leg_joint_x, leg_joint_y), (right_foot_x, foot_y), 4)

    # วาดเท้า
    pygame.draw.ellipse(screen, DARK_BROWN, (left_foot_x - 5, foot_y, 10, 5))  # เท้าซ้าย
    pygame.draw.ellipse(screen, DARK_BROWN, (right_foot_x - 5, foot_y, 10, 5))  # เท้าขวา

    # คันธนู
    bow_radius = 30
    bow_color = (139, 69, 19)
    bow_string_color = (255, 255, 240)
    
    # คำนวณตำแหน่งของคันธนูตามมุม
    bow_x = bow_arm_x
    bow_y = bow_arm_y
    
    # คำนวณมุมเริ่มต้นและสิ้นสุดของส่วนโค้งของคันธนูตามทิศทาง
    bow_center_angle = angle  # มุมกลางของคันธนู
    bow_start_angle = math.radians(bow_center_angle - 30)
    bow_end_angle = math.radians(bow_center_angle + 30)

    # วาดคันธนู (หนาขึ้นด้วยหลายเส้น)
    for i in range(5):
        offset = i - 2
        pygame.draw.arc(screen, bow_color, 
                        (bow_x - bow_radius + offset, bow_y - bow_radius + offset, 
                         bow_radius * 2, bow_radius * 2),
                        bow_start_angle, bow_end_angle, 2)

    # วาดสายธนู
    string_start_x = bow_x + bow_radius * 0.85 * math.cos(bow_start_angle)
    string_start_y = bow_y + bow_radius * 0.85 * math.sin(bow_start_angle)
    string_end_x = bow_x + bow_radius * 0.85 * math.cos(bow_end_angle)
    string_end_y = bow_y + bow_radius * 0.85 * math.sin(bow_end_angle)
    
    # จุดกลางของสายธนูสำหรับการดึง
    if draw_arrow:
        # สายธนูที่ไม่ได้ถูกดึง - สายธนูหันไปในทิศทางเดียวกับลูกธนู
        pygame.draw.line(screen, bow_string_color, (string_start_x, string_start_y), (string_end_x, string_end_y), 1)
    else:
        # สายธนูถูกดึง - สายธนูหันไปในทิศทางเดียวกับลูกธนู
        mid_x = bow_x + math.cos(math.radians(angle)) * 15
        mid_y = bow_y + math.sin(math.radians(angle)) * 15
        pygame.draw.line(screen, bow_string_color, (string_start_x, string_start_y), (mid_x, mid_y), 1)
        pygame.draw.line(screen, bow_string_color, (mid_x, mid_y), (string_end_x, string_end_y), 1)
    
    # วาดลูกธนูที่อยู่บนคันธนูเมื่อไม่ได้ยิง
    if draw_arrow:
        # คำนวณตำแหน่งกลางของลูกธนูบนคันธนู
        arrow_x = bow_x + math.cos(math.radians(angle)) * 15
        arrow_y = bow_y + math.sin(math.radians(angle)) * 15
        
        # วาดลูกธนูที่หมุนตามมุม
        rotated_arrow = pygame.transform.rotate(arrow_img, -angle)
        arrow_rect = rotated_arrow.get_rect(center=(arrow_x, arrow_y))
        screen.blit(rotated_arrow, arrow_rect.topleft)

def draw_target(target_x, target_y, target_radius):
    """วาดเป้าหมายละเอียดพร้อมขาตั้งไม้"""
    # ขาตั้งเป้า
    stand_width = 20
    stand_color = DARK_BROWN
    stand_light_color = LIGHT_BROWN

    # ขาตั้งไม้พร้อมลวดลาย
    pygame.draw.rect(screen, stand_color, (target_x - stand_width/2, target_y, stand_width, HEIGHT - target_y - 100))

    # เพิ่มลายไม้
    for i in range(5):
        y_pos = target_y + i * 30
        if y_pos < HEIGHT - 100:
            pygame.draw.line(screen, stand_light_color, 
                            (target_x - stand_width/2, y_pos), 
                            (target_x + stand_width/2, y_pos), 1)

    # เงาใต้เป้าหมาย
    pygame.draw.ellipse(screen, (70, 40, 0), (target_x - target_radius, target_y + target_radius*0.9, target_radius*2, target_radius*0.3))

    # วงแหวนเป้าหมายพร้อมเอฟเฟกต์ 3 มิติ
    for radius, color in target_rings:
        pygame.draw.circle(screen, color, (target_x, target_y), radius)
        # เพิ่มไฮไลท์สำหรับเอฟเฟกต์ 3 มิติ (ใช้สีขาวล้วน)
        if radius > target_radius * 0.2:  # ไม่เพิ่มไฮไลท์ให้กับจุดกลาง
            try:
                # ใช้สีที่ถูกต้องตามรูปแบบ RGB (ไม่ใช้ alpha)
                pygame.draw.arc(screen, (255, 255, 255), 
                              (target_x - radius, target_y - radius, radius*2, radius*2),
                              math.radians(45), math.radians(135), 2)
            except pygame.error as e:
                print(f"ข้อผิดพลาดในการวาดไฮไลท์เป้า: {e}")

def calculate_distance(x1, y1, x2, y2):
    """คำนวณระยะห่างระหว่างสองจุด"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def is_point_in_ellipse(x, y, ellipse_x, ellipse_y, width, height):
    """ตรวจสอบว่าจุดอยู่ภายในวงรีหรือไม่"""
    # ตรวจสอบว่าพิกัดมีค่าที่ถูกต้อง
    if (math.isnan(x) or math.isnan(y) or 
        math.isnan(ellipse_x) or math.isnan(ellipse_y) or
        math.isnan(width) or math.isnan(height) or
        width <= 0 or height <= 0):
        return False

    # ปรับพิกัดให้ตรงกับจุดศูนย์กลางวงรี
    nx = x - (ellipse_x + width/2)
    ny = y - (ellipse_y + height/2)

    # ป้องกันการหารด้วยศูนย์
    try:
        # ตรวจสอบว่าจุดอยู่ภายในวงรีหรือไม่
        return (nx**2 / (width/2)**2) + (ny**2 / (height/2)**2) <= 1
    except ZeroDivisionError:
        return False

def draw_cloud(x, y, width, height):
    """วาดเมฆฟูฟ่องพร้อมไล่ระดับสีและรายละเอียด"""
    try:
        # ตรวจสอบความถูกต้องของค่าพารามิเตอร์
        if width <= 0 or height <= 0:
            return

        # ชั้นของเมฆเพื่อความสมจริงมากขึ้น
        cloud_layers = [
            (0, 0, width, height),
            (-width/4, height/4, width/2, height/2),
            (width/2, height/4, width/2, height/2),
            (width/4, -height/5, width/2, height/2),
            (width/10, height/3, width/3, height/3)
        ]

        # วาดแกนหลักของเมฆพร้อมไล่ระดับสี
        for layer in cloud_layers:
            base_x, base_y, layer_width, layer_height = layer
            # ตรวจสอบว่าขนาดไม่ติดลบ
            if layer_width <= 0 or layer_height <= 0:
                continue

            for i in range(4):  # หลายชั้นสำหรับเอฟเฟกต์ไล่ระดับสี
                cloud_shade = (min(255, CLOUD_COLOR[0] - i*5), 
                               min(255, CLOUD_COLOR[1] - i*5), 
                               min(255, CLOUD_COLOR[2] - i*5))
                try:
                    pygame.draw.ellipse(screen, cloud_shade,
                                     (int(x + base_x), int(y + base_y), 
                                      max(1, int(layer_width)), 
                                      max(1, int(layer_height))))
                except pygame.error:
                    pass  # ข้ามการวาดหากเกิดข้อผิดพลาด

        # เพิ่มไฮไลท์เพื่อให้เมฆดูมีปริมาตร
        if width > 0 and height > 0:
            highlight_color = (250, 250, 250)
            try:
                pygame.draw.ellipse(screen, highlight_color,
                                  (int(x + width/8), int(y + height/8), 
                                   max(1, int(width/4)), 
                                   max(1, int(height/4))))
            except pygame.error:
                pass  # ข้ามการวาดหากเกิดข้อผิดพลาด

        # ขอบบางๆ เพื่อความชัดเจน
        border_color = (220, 220, 220)
        for layer in cloud_layers:
            base_x, base_y, layer_width, layer_height = layer
            if layer_width > 0 and layer_height > 0:
                try:
                    pygame.draw.ellipse(screen, border_color,
                                      (int(x + base_x), int(y + base_y), 
                                       max(1, int(layer_width)), 
                                       max(1, int(layer_height))), 1)
                except pygame.error:
                    pass  # ข้ามการวาดหากเกิดข้อผิดพลาด
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการวาดเมฆ: {e}")

# ฟังก์ชันสำหรับวาดสี่เหลี่ยมขอบมน
def draw_rounded_rect(surface, color, rect, radius=15, border_width=0):
    """วาดสี่เหลี่ยมขอบมน"""
    rect = pygame.Rect(rect)

    # ตรวจสอบว่ารัศมีไม่เกินครึ่งของความกว้างและความสูง
    radius = min(radius, rect.width//2, rect.height//2)

    # วาดพื้นที่หลัก
    if border_width == 0:  # วาดพื้นที่สี่เหลี่ยมทั้งหมด
        pygame.draw.rect(surface, color, rect.inflate(-radius*2, 0))
        pygame.draw.rect(surface, color, rect.inflate(0, -radius*2))

        # วาดมุมทั้งสี่
        pygame.draw.circle(surface, color, (rect.left + radius, rect.top + radius), radius)
        pygame.draw.circle(surface, color, (rect.right - radius, rect.top + radius), radius)
        pygame.draw.circle(surface, color, (rect.left + radius, rect.bottom - radius), radius)
        pygame.draw.circle(surface, color, (rect.right - radius, rect.bottom - radius), radius)
    else:  # วาดเฉพาะขอบ
        pygame.draw.rect(surface, color, rect.inflate(-radius*2, 0), border_width)
        pygame.draw.rect(surface, color, rect.inflate(0, -radius*2), border_width)

        # วาดส่วนโค้งของมุม
        pygame.draw.arc(surface, color, (rect.left, rect.top, radius*2, radius*2), 
                      math.radians(180), math.radians(270), border_width)
        pygame.draw.arc(surface, color, (rect.right-radius*2, rect.top, radius*2, radius*2), 
                      math.radians(270), math.radians(360), border_width)
        pygame.draw.arc(surface, color, (rect.left, rect.bottom-radius*2, radius*2, radius*2), 
                      math.radians(90), math.radians(180), border_width)
        pygame.draw.arc(surface, color, (rect.right-radius*2, rect.bottom-radius*2, radius*2, radius*2), 
                      math.radians(0), math.radians(90), border_width)

def draw_instructions(show_controls=True):
    """วาดคำแนะนำการเล่นเกมพร้อมกล่องสไตล์"""
    if not show_controls:
        return

    # วาดพื้นหลังทึบสำหรับคำแนะนำ
    try:
        # วาดกล่องพื้นหลังสีดำ
        draw_rounded_rect(screen, (0, 0, 0), (10, 10, 200, 185), radius=10)

        # เพิ่มขอบสีขาว
        draw_rounded_rect(screen, WHITE, (10, 10, 200, 185), radius=10, border_width=1)
    except pygame.error as e:
        print(f"ข้อผิดพลาดในการวาดกล่องคำแนะนำ: {e}")
        # ใช้สี่เหลี่ยมธรรมดาแทนถ้าเกิดข้อผิดพลาด
        try:
            pygame.draw.rect(screen, (0, 0, 0), (10, 10, 200, 185))
            pygame.draw.rect(screen, WHITE, (10, 10, 200, 185), 1)
        except pygame.error:
            pass  # ข้ามหากยังมีข้อผิดพลาด

    # หัวข้อ
    title_font = pygame.font.SysFont('Arial', 20, bold=True)
    title_surf = title_font.render("Controls:", True, WHITE)
    screen.blit(title_surf, (20, 15))

    # คำแนะนำพร้อมไอคอน
    instructions = [
        "↑/↓: Adjust angle",
        "←/→: Adjust power",
        "SPACE: Shoot arrow",
        "+/-: Increase/decrease FPS",
        "F: Show/hide FPS",
        "H: Show/hide controls",
        "ESC: Back to main menu"
    ]

    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (20, 45 + i * 25))

def draw_start_screen():
    """วาดหน้าจอเริ่มต้นแบบเคลื่อนไหวและมีรายละเอียด"""
    # พื้นหลังด้วยท้องฟ้าไล่ระดับสี
    for y in range(HEIGHT):
        depth = 1 - (y / HEIGHT * 0.8)
        sky_color = (int(135 * depth), int(206 * depth), int(235 * depth))
        pygame.draw.line(screen, sky_color, (0, y), (WIDTH, y))

    # เมฆเคลื่อนที่ในพื้นหลัง (สำหรับตกแต่ง)
    time_offset = pygame.time.get_ticks() / 1000
    for i in range(3):
        cloud_x = ((time_offset * 20) + i * WIDTH/3) % (WIDTH + 200) - 100
        cloud_y = HEIGHT/8 + i * HEIGHT/10
        draw_cloud(cloud_x, cloud_y, 120, 60)

    # พระอาทิตย์พร้อมรังสี
    pygame.draw.circle(screen, GOLDEN, (WIDTH - 100, 100), 40)
    for angle in range(0, 360, 30):
        end_x = WIDTH - 100 + math.cos(math.radians(angle)) * 60
        end_y = 100 + math.sin(math.radians(angle)) * 60
        pygame.draw.line(screen, GOLDEN, (WIDTH - 100, 100), (end_x, end_y), 2)

    # หญ้าพร้อมลวดลาย
    pygame.draw.rect(screen, GRASS_GREEN, (0, HEIGHT - 100, WIDTH, 100))
    # เพิ่มรายละเอียดหญ้า
    for i in range(0, WIDTH, 10):
        grass_height = random.randint(5, 15)
        grass_x_offset = math.sin(time_offset + i/50) * 3  # เอฟเฟกต์คลื่นนุ่มนวล
        pygame.draw.line(screen, (45, 160, 45), 
                       (i + grass_x_offset, HEIGHT - 100), 
                       (i, HEIGHT - 100 - grass_height), 2)

    # ชื่อเกมพร้อมเอฟเฟกต์เงา
    title_font = pygame.font.SysFont('Arial', 70, bold=True)
    shadow_text = title_font.render("Archery Challenge", True, (50, 30, 10))
    title_text = title_font.render("Archery Challenge", True, DARK_BROWN)

    screen.blit(shadow_text, (WIDTH // 2 - shadow_text.get_width() // 2 + 4, HEIGHT // 3 + 4))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

    # วาดคันธนูและลูกธนูพร้อมภาพเคลื่อนไหว
    bow_x, bow_y = WIDTH // 2, HEIGHT // 2 - 30
    time_val = pygame.time.get_ticks() / 1000  # สำหรับภาพเคลื่อนไหว
    bow_pull = abs(math.sin(time_val * 2)) * 10  # ดึงคันธนูเคลื่อนไหว

    # คันธนูพร้อมภาพเคลื่อนไหว
    pygame.draw.arc(screen, BROWN, 
                  (bow_x - 50, bow_y - 50, 100, 100),
                  math.radians(-30), math.radians(30), 4)

    # สายธนูพร้อมภาพเคลื่อนไหว
    string_start_x = bow_x - 40 + bow_pull
    string_end_x = bow_x + 40 - bow_pull
    pygame.draw.line(screen, WHITE, (string_start_x, bow_y - 30), (bow_x, bow_y), 2)
    pygame.draw.line(screen, WHITE, (string_end_x, bow_y - 30), (bow_x, bow_y), 2)

    # ลูกธนู
    pygame.draw.line(screen, DARK_BROWN, (bow_x - 40 + bow_pull, bow_y), (bow_x + 40, bow_y), 3)

    # หัวลูกธนู
    pygame.draw.polygon(screen, DARK_RED, [(bow_x + 40, bow_y),
                                         (bow_x + 50, bow_y - 5),
                                         (bow_x + 50, bow_y + 5)])

    # ปุ่มเริ่มเกมพร้อมเอฟเฟกต์เต้นตามจังหวะ
    button_width, button_height = 200, 60
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT * 3 // 4

    # ภาพเคลื่อนไหวเต้นตามจังหวะของปุ่ม
    pulse = math.sin(time_val * 4) * 5
    button_glow = max(0, int(pulse * 20))

    # ปุ่มพร้อมเงา
    try:
        # เงาของปุ่ม
        draw_rounded_rect(screen, (100, 0, 0), 
                        (button_x - 5, button_y - 3, button_width + 10, button_height + 6),
                        radius=15)

        # ปุ่มหลัก - จำกัดค่าสีไม่ให้เกิน 255
        draw_rounded_rect(screen, (min(255, DARK_RED[0] + button_glow), DARK_RED[1], DARK_RED[2]),
                        (button_x, button_y, button_width, button_height),
                        radius=12)

        draw_rounded_rect(screen, (min(255, RED[0] + button_glow), RED[1], RED[2]),
                        (button_x + 4, button_y + 4, button_width - 8, button_height - 8),
                        radius=10)
    except pygame.error as e:
        print(f"ข้อผิดพลาดในการวาดปุ่ม: {e}")
        # ใช้สีพื้นฐานถ้าเกิดข้อผิดพลาด
        try:
            draw_rounded_rect(screen, DARK_RED, (button_x, button_y, button_width, button_height), radius=12)
            draw_rounded_rect(screen, RED, (button_x + 4, button_y + 4, button_width - 8, button_height - 8), radius=10)
        except pygame.error:
            pass

    # ขอบปุ่ม
    draw_rounded_rect(screen, WHITE, 
                    (button_x, button_y, button_width, button_height), 
                    radius=12, border_width=2)

    # ข้อความบนปุ่มพร้อมเอฟเฟกต์เรืองแสง
    start_font = pygame.font.SysFont('Arial', 30, bold=True)
    start_text = start_font.render("Start Game", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, button_y + button_height // 2))

    # เอฟเฟกต์เรืองแสงของข้อความ
    glow_text = start_font.render("Start Game", True, (255, 255, 200))
    glow_rect = glow_text.get_rect(center=(WIDTH // 2, button_y + button_height // 2))

    if pulse > 0:
        screen.blit(glow_text, (glow_rect.x, glow_rect.y))
    screen.blit(start_text, start_rect)

    # คำแนะนำพร้อมกล่องตกแต่ง
    try:
        # วาดพื้นหลังทึบสำหรับคำแนะนำ
        draw_rounded_rect(screen, (0, 0, 0), 
                       (WIDTH // 2 - 200, button_y + button_height + 20, 400, 80),
                       radius=15)

        # เพิ่มขอบสีขาวล้อมรอบ
        draw_rounded_rect(screen, WHITE, 
                        (WIDTH // 2 - 200, button_y + button_height + 20, 400, 80),
                        radius=15, border_width=1)

    except pygame.error as e:
        print(f"ข้อผิดพลาดในการสร้าง Surface สำหรับคำแนะนำ: {e}")
        # ใช้รูปแบบที่เรียบง่ายกว่าถ้าเกิดข้อผิดพลาด
        try:
            pygame.draw.rect(screen, (0, 0, 0), 
                         (WIDTH // 2 - 200, button_y + button_height + 20, 400, 80))
            pygame.draw.rect(screen, WHITE, 
                         (WIDTH // 2 - 200, button_y + button_height + 20, 400, 80), 1)
        except pygame.error:
            pass  # ข้ามหากยังมีข้อผิดพลาด

    # คำแนะนำ
    instruction_font = pygame.font.SysFont('Arial', 18)
    instruction_text = instruction_font.render("Click button to start playing!", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, button_y + button_height + 40))
    screen.blit(instruction_text, instruction_rect)

    # คำแนะนำเพิ่มเติมเกี่ยวกับเมฆและเป้าเคลื่อนที่
    cloud_text = instruction_font.render("Watch out for moving clouds blocking your arrows!", True, WHITE)
    cloud_rect = cloud_text.get_rect(center=(WIDTH // 2, button_y + button_height + 60))
    screen.blit(cloud_text, cloud_rect)

    # คำแนะนำเกี่ยวกับเป้าเคลื่อนที่
    target_text = instruction_font.render("Hit the moving target for extra challenge!", True, WHITE)
    target_rect = target_text.get_rect(center=(WIDTH // 2, button_y + button_height + 85))
    screen.blit(target_text, target_rect)

    # เพิ่มเป้าหมายตกแต่งในพื้นหลัง
    for i in range(3):
        mini_target_x = 100 + i * 300
        mini_target_y = HEIGHT - 150 + i * 20
        mini_radius = 20
        for j, (radius_factor, color) in enumerate(target_rings):
            radius = mini_radius * radius_factor / target_radius
            pygame.draw.circle(screen, color, (mini_target_x, mini_target_y), radius)

    return button_x, button_y, button_width, button_height

def main():
    """ลูปเกมหลัก"""
    running = True
    in_start_screen = True

    # ตัวแปรเกม
    target_x = random.randint(600, 750)
    target_y = HEIGHT - 150
    archer_x, archer_y = 100, HEIGHT - 160  # ตำแหน่งของนักยิงธนูเหนือพื้นหญ้า 40 หน่วย (HEIGHT - 160 แทน HEIGHT - 220)
    arrow_x, arrow_y = archer_x, archer_y  # ตำแหน่งเริ่มต้นของลูกธนู
    angle = 0  # มุมการยิง
    shooting = False  # สถานะการยิง
    velocity = 0  # ความเร็วลูกธนู
    hit = False  # ตรวจสอบการโดน
    score = 0
    shots = 0
    flight_time = 0  # เวลาที่ลูกธนูอยู่ในอากาศ (สำหรับคำนวณแรงโน้มถ่วง)

    # FPS settings
    current_fps = 60
    min_fps = 30
    max_fps = 120

    # Controls visibility
    show_controls = True

    # ตัวแปรการเปลี่ยนแรง
    base_velocity = 250
    force_variation = 0
    last_force_change_time = pygame.time.get_ticks()
    force_change_interval = 10000  # 10000ms = 10 นาที (สำหรับทดสอบ, จริงๆ 10 นาทีคือ 600000)

    # ตัวแปรการเคลื่อนที่ของเป้าหมาย
    target_speed = 2  # ความเร็วการเคลื่อนที่ของเป้า
    target_direction = 1  # ทิศทางการเคลื่อนที่ (1 = ลง, -1 = ขึ้น)
    target_min_y = HEIGHT - 250  # จุดสูงสุดที่เป้าเคลื่อนที่ขึ้นได้
    target_max_y = HEIGHT - 100  # จุดต่ำสุดที่เป้าเคลื่อนที่ลงได้

    #ตัวแปรเมฆ
    cloud_x = WIDTH + 100  # เริ่มต้นออกนอกหน้าจอ
    cloud_y = HEIGHT // 3
    cloud_width = 180
    cloud_height = 80
    cloud_speed = 2
    cloud_direction = -1  # เคลื่อนที่ไปทางซ้าย

    while running:
        if in_start_screen:
            # วาดหน้าจอเริ่มต้นและรับตำแหน่งปุ่ม
            button_x, button_y, button_width, button_height = draw_start_screen()

            # ตรวจสอบอีเวนต์
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # ตรวจสอบว่าคลิกปุ่มเริ่มเกมหรือไม่
                    if (button_x <= mouse_x <= button_x + button_width and 
                        button_y <= mouse_y <= button_y + button_height):
                        in_start_screen = False
                        # รีเซ็ตเวลาเกมเมื่อเริ่มเล่น
                        last_force_change_time = pygame.time.get_ticks()
        else:
            # เกมหลัก
            draw_background()

            # อัพเดตตำแหน่งเป้าหมาย (เคลื่อนที่ขึ้นลง)
            target_y += target_speed * target_direction

            # เปลี่ยนทิศทางเมื่อเป้าหมายถึงขอบบนหรือล่าง
            if target_y <= target_min_y:
                target_direction = 1  # เปลี่ยนทิศทางเป็นลง
                target_y = target_min_y  # ป้องกันไม่ให้เป้าออกนอกขอบเขต
            elif target_y >= target_max_y:
                target_direction = -1  # เปลี่ยนทิศทางเป็นขึ้น
                target_y = target_max_y  # ป้องกันไม่ให้เป้าออกนอกขอบเขต

            draw_target(target_x, target_y, target_radius)

            # อัพเดตและวาดเมฆ
            cloud_x += cloud_speed * cloud_direction
            # เปลี่ยนทิศทางเมื่อเมฆถึงขอบหน้าจอ
            if cloud_x < -cloud_width:
                cloud_x = WIDTH
                cloud_y = random.randint(HEIGHT // 5, HEIGHT // 2)
            elif cloud_x > WIDTH:
                cloud_x = -cloud_width
                cloud_y = random.randint(HEIGHT // 5, HEIGHT // 2)

            draw_cloud(cloud_x, cloud_y, cloud_width, cloud_height)
            # ไม่ต้องวาดนักยิงธนูที่นี่เพราะจะวาดหลังจากคำนวณตำแหน่งลูกธนูแล้ว
            draw_instructions(show_controls)

            # แสดงคะแนน
            score_text = font.render(f"Score: {score} | Shots: {shots}", True, BLACK)
            force_text = font.render(f"Power: {base_velocity - force_variation} m/h", True, BLACK)
            fps_text = font.render(f"FPS: {current_fps}", True, BLACK)
            screen.blit(score_text, (WIDTH - 200, 20))
            screen.blit(force_text, (WIDTH - 200, 50))
            screen.blit(fps_text, (WIDTH - 200, 80))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        angle = min(angle + 5, 70)  # จำกัดมุมสูงสุด
                    elif event.key == pygame.K_DOWN:
                        angle = max(angle - 5, -20)  # จำกัดมุมต่ำสุด
                    elif event.key == pygame.K_LEFT:
                        # ลดความแรง
                        base_velocity = max(250, base_velocity - 10)
                    elif event.key == pygame.K_RIGHT:
                        # เพิ่มความแรง
                        base_velocity = min(370, base_velocity + 10)
                    elif event.key == pygame.K_SPACE and not shooting:
                        shooting = True
                        velocity = (base_velocity - force_variation) / 16.67  # ปรับสเกลให้เหมาะสมกับความเร็วที่เพิ่มขึ้น
                        shots += 1
                        # ตั้งตำแหน่งเริ่มต้นของลูกธนูให้ตรงกับตำแหน่งนักยิง
                        arrow_x, arrow_y = archer_x, archer_y
                        # รีเซ็ตเวลาในการบิน
                        flight_time = 0
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS or event.key == pygame.K_EQUALS:
                        # เพิ่ม FPS
                        current_fps = min(max_fps, current_fps + 10)
                        print(f"FPS increased to {current_fps}")
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        # ลด FPS
                        current_fps = max(min_fps, current_fps - 10)
                        print(f"FPS decreased to {current_fps}")
                    elif event.key == pygame.K_h:
                        # Toggle controls visibility
                        show_controls = not show_controls
                        print(f"Controls visibility: {'shown' if show_controls else 'hidden'}")
                    elif event.key == pygame.K_ESCAPE:
                        # กลับสู่หน้าจอเริ่มต้น
                        in_start_screen = True
                        # รีเซ็ตตัวแปรเกม
                        archer_x, archer_y = 100, HEIGHT - 160
                        arrow_x, arrow_y = archer_x, archer_y
                        angle = 0
                        shooting = False
                        target_x = random.randint(600, 750)


            if shooting:
                try:
                    # เพิ่มเวลาในการบิน
                    flight_time += 1/60  # เพิ่มเวลาตามจำนวนเฟรมต่อวินาที

                    # คำนวณการเคลื่อนที่ของลูกธนู
                    # ค่าปรับเพื่อให้แรงโน้มถ่วงทำงานได้เหมาะสมกับค่าความเร็ว
                    time_scale = 0.05  

                    # คำนวณการเคลื่อนที่ในแนวนอน (ไม่มีแรงโน้มถ่วงในแนวนอน)
                    arrow_x += velocity * math.cos(math.radians(angle))

                    # คำนวณการเคลื่อนที่ในแนวตั้ง โดยใช้แรงโน้มถ่วง 10 m/s²
                    # ความเร็วในแนวตั้งเริ่มต้น - แรงโน้มถ่วง * เวลา
                    vertical_velocity = velocity * math.sin(math.radians(angle)) - GRAVITY * flight_time * time_scale
                    arrow_y -= vertical_velocity  # เคลื่อนที่ตามความเร็วในแนวตั้งปัจจุบัน

                    # คำนวณมุมของลูกธนูตามทิศทางการเคลื่อนที่
                    # คำนวณเวกเตอร์ความเร็วในแนวราบและแนวดิ่ง
                    horizontal_velocity = velocity * math.cos(math.radians(angle))
                    current_vertical_velocity = vertical_velocity

                    # คำนวณมุมของลูกธนูจากเวกเตอร์ความเร็ว (ทิศทางการเคลื่อนที่)
                    arrow_angle = math.degrees(math.atan2(-current_vertical_velocity, horizontal_velocity))

                    # ตรวจสอบว่าค่าพิกัดมีความถูกต้อง (ไม่เป็น NaN หรือ infinity)
                    if math.isnan(arrow_x) or math.isnan(arrow_y) or math.isinf(arrow_x) or math.isinf(arrow_y):
                        print("พบค่าผิดปกติในการคำนวณตำแหน่งลูกธนู")
                        shooting = False
                        # ตำแหน่งลูกธนูจะถูกรีเซ็ตอัตโนมัติจากการวาดคันธนู
                        continue

                    # ตรวจสอบการชนกับเมฆ
                    cloud_collision = False
                    if (cloud_x > -cloud_width and cloud_x < WIDTH):  # เมฆอยู่ในหน้าจอ
                        cloud_collision = (
                            is_point_in_ellipse(arrow_x, arrow_y, cloud_x, cloud_y, cloud_width, cloud_height) or
                            is_point_in_ellipse(arrow_x, arrow_y, cloud_x - cloud_width/4, cloud_y + cloud_height/4, cloud_width/2, cloud_height/2) or
                            is_point_in_ellipse(arrow_x, arrow_y, cloud_x + cloud_width/2, cloud_y + cloud_height/4, cloud_width/2, cloud_height/2)
                        )

                    if cloud_collision:
                        shooting = False
                        # ตำแหน่งลูกธนูจะถูกรีเซ็ตอัตโนมัติจากการวาดคันธนู
                        print("ลูกธนูชนเมฆ!")
                        continue

                    distance = calculate_distance(arrow_x, arrow_y, target_x, target_y)

                    if distance < target_radius:
                        hit = True
                        shooting = False

                        # คำนวณคะแนนตามความใกล้เคียงกับศูนย์กลาง
                        ring_score = 5
                        for ring_radius, _ in target_rings:
                            if distance < ring_radius:
                                score += ring_score
                                break
                            ring_score -= 1

                        print(f"โดน! คะแนน: {score}")
                        # ตำแหน่งลูกธนูจะถูกรีเซ็ตอัตโนมัติจากการวาดคันธนู
                    elif arrow_x > WIDTH or arrow_y < 0 or arrow_y > HEIGHT:
                        shooting = False
                        # ตำแหน่งลูกธนูจะถูกรีเซ็ตอัตโนมัติจากการวาดคันธนู
                except Exception as e:
                    print(f"เกิดข้อผิดพลาดในการคำนวณการเคลื่อนที่ของลูกธนู: {e}")
                    shooting = False
                    # ตำแหน่งลูกธนูจะถูกรีเซ็ตอัตโนมัติจากการวาดคันธนู

            # วาดนักยิงธนูโดยไม่มีลูกธนูบนคันธนูขณะยิง
            draw_archer(archer_x, archer_y, angle, not shooting)
            
            # วาดรอยของลูกธนูขณะยิง
            if shooting:
                for i in range(1, 5):
                    trace_x = arrow_x - i * 8 * math.cos(math.radians(angle))
                    trace_y = arrow_y + i * 8 * math.sin(math.radians(angle))
                    # ตรวจสอบว่าพิกัดมีค่าที่ถูกต้อง
                    if not (math.isnan(trace_x) or math.isnan(trace_y)):
                        try:
                            pygame.draw.circle(screen, (200, 200, 200), (int(trace_x), int(trace_y)), 2)
                        except pygame.error:
                            pass  # ข้ามการวาดหากเกิดข้อผิดพลาด

                # วาดลูกธนูที่หันตามทิศทางการเคลื่อนที่
                rotated_arrow = pygame.transform.rotate(arrow_img, -arrow_angle)
                arrow_rect = rotated_arrow.get_rect(center=(arrow_x, arrow_y))
                screen.blit(rotated_arrow, arrow_rect.topleft)

        pygame.display.flip()
        clock.tick(current_fps)

    # ตรวจสอบว่า pygame ยังทำงานอยู่ไหมก่อนออกจากเกม
    try:
        pygame.quit()
        print("ปิด Pygame เรียบร้อย")
    except:
        print("เกิดข้อผิดพลาดขณะปิด Pygame")

if __name__ == "__main__":
    try:
        print(f"เริ่มต้นเกม - Pygame เวอร์ชัน: {pygame.version.ver}")
        main()
    except Exception as e:
        print(f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")
        pygame.quit()
