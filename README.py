
import pygame
import math
import random

# เริ่มต้น Pygame
pygame.init()

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

# การตั้งค่าหน้าจอ
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Archery Game")
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
    # รัศมีพระอาทิตย์
    for radius in range(45, 60, 5):
        pygame.draw.circle(screen, (255, 215, 0, 100-radius), (sun_x, sun_y), radius, 2)
    
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

def draw_archer(x, y, angle):
    """วาดตัวนักยิงธนูที่มีรายละเอียดมากขึ้น"""
    # ลำตัว
    body_color = (80, 60, 40)
    pygame.draw.line(screen, body_color, (x - 30, y), (x - 30, y + 40), 5)
    
    # ศีรษะ
    head_color = (210, 180, 140)
    pygame.draw.circle(screen, head_color, (x - 30, y - 10), 8)
    
    # แขน
    pygame.draw.line(screen, body_color, (x - 30, y + 10), (x - 5, y), 4)
    pygame.draw.line(screen, body_color, (x - 30, y + 10), (x - 10, y + 15), 4)
    
    # ขา
    pygame.draw.line(screen, body_color, (x - 30, y + 40), (x - 35, y + 55), 4)
    pygame.draw.line(screen, body_color, (x - 30, y + 40), (x - 25, y + 55), 4)
    
    # คันธนู
    bow_radius = 30
    bow_color = (139, 69, 19)
    bow_string_color = (255, 255, 240)
    bow_start_angle = math.radians(angle - 30)
    bow_end_angle = math.radians(angle + 30)
    
    # วาดคันธนู (หนาขึ้นด้วยหลายเส้น)
    for i in range(5):
        offset = i - 2
        pygame.draw.arc(screen, bow_color, 
                        (x - bow_radius + offset, y - bow_radius + offset, 
                         bow_radius * 2, bow_radius * 2),
                        bow_start_angle, bow_end_angle, 2)
    
    # วาดสายธนู
    string_start_x = x + bow_radius * 0.85 * math.cos(bow_start_angle)
    string_start_y = y + bow_radius * 0.85 * math.sin(bow_start_angle)
    string_end_x = x + bow_radius * 0.85 * math.cos(bow_end_angle)
    string_end_y = y + bow_radius * 0.85 * math.sin(bow_end_angle)
    pygame.draw.line(screen, bow_string_color, (string_start_x, string_start_y), (string_end_x, string_end_y), 1)

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
    shadow_color = (0, 0, 0, 50)  # สีดำโปร่งแสง
    pygame.draw.ellipse(screen, (70, 40, 0), (target_x - target_radius, target_y + target_radius*0.9, target_radius*2, target_radius*0.3))
    
    # วงแหวนเป้าหมายพร้อมเอฟเฟกต์ 3 มิติ
    for radius, color in target_rings:
        pygame.draw.circle(screen, color, (target_x, target_y), radius)
        # เพิ่มไฮไลท์สำหรับเอฟเฟกต์ 3 มิติ
        if radius > target_radius * 0.2:  # ไม่เพิ่มไฮไลท์ให้กับจุดกลาง
            pygame.draw.arc(screen, (255, 255, 255, 100), 
                          (target_x - radius, target_y - radius, radius*2, radius*2),
                          math.radians(45), math.radians(135), 2)

def calculate_distance(x1, y1, x2, y2):
    """คำนวณระยะห่างระหว่างสองจุด"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def is_point_in_ellipse(x, y, ellipse_x, ellipse_y, width, height):
    """ตรวจสอบว่าจุดอยู่ภายในวงรีหรือไม่"""
    # ปรับพิกัดให้ตรงกับจุดศูนย์กลางวงรี
    nx = x - (ellipse_x + width/2)
    ny = y - (ellipse_y + height/2)
    
    # ตรวจสอบว่าจุดอยู่ภายในวงรีหรือไม่
    return (nx**2 / (width/2)**2) + (ny**2 / (height/2)**2) <= 1

def draw_cloud(x, y, width, height):
    """วาดเมฆฟูฟ่องพร้อมไล่ระดับสีและรายละเอียด"""
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
        for i in range(4):  # หลายชั้นสำหรับเอฟเฟกต์ไล่ระดับสี
            opacity = 220 - i * 20
            cloud_shade = (min(255, CLOUD_COLOR[0] - i*5), 
                           min(255, CLOUD_COLOR[1] - i*5), 
                           min(255, CLOUD_COLOR[2] - i*5))
            pygame.draw.ellipse(screen, cloud_shade,
                              (x + base_x, y + base_y, layer_width, layer_height))
    
    # เพิ่มไฮไลท์เพื่อให้เมฆดูมีปริมาตร
    highlight_color = (250, 250, 250)
    pygame.draw.ellipse(screen, highlight_color,
                      (x + width/8, y + height/8, width/4, height/4))
    
    # ขอบบางๆ เพื่อความชัดเจน
    border_color = (220, 220, 220)
    for layer in cloud_layers:
        base_x, base_y, layer_width, layer_height = layer
        pygame.draw.ellipse(screen, border_color,
                          (x + base_x, y + base_y, layer_width, layer_height), 1)

def draw_instructions():
    """วาดคำแนะนำการเล่นเกมพร้อมกล่องสไตล์"""
    # วาดพื้นหลังโปร่งแสงสำหรับคำแนะนำ
    instruction_bg = pygame.Surface((200, 110), pygame.SRCALPHA)
    instruction_bg.fill((0, 0, 0, 100))  # สีดำโปร่งแสง
    screen.blit(instruction_bg, (10, 10))
    
    # เพิ่มขอบ
    pygame.draw.rect(screen, WHITE, (10, 10, 200, 110), 1)
    
    # หัวข้อ
    title_font = pygame.font.SysFont('Arial', 20, bold=True)
    title_surf = title_font.render("ควบคุม:", True, WHITE)
    screen.blit(title_surf, (20, 15))
    
    # คำแนะนำพร้อมไอคอน
    instructions = [
        "↑/↓: ปรับมุมยิง",
        "SPACE: ยิงลูกธนู",
        "ESC: กลับสู่เมนูหลัก"
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
    shadow_text = title_font.render("ท้าทายการยิงธนู", True, (50, 30, 10))
    title_text = title_font.render("ท้าทายการยิงธนู", True, DARK_BROWN)
    
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
    pygame.draw.rect(screen, (100, 0, 0), 
                   (button_x - 5, button_y - 3, button_width + 10, button_height + 6))
    
    # ปุ่มหลัก
    pygame.draw.rect(screen, (DARK_RED[0] + button_glow, DARK_RED[1], DARK_RED[2]),
                   (button_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, (RED[0] + button_glow, RED[1], RED[2]),
                   (button_x + 4, button_y + 4, button_width - 8, button_height - 8))
    
    # ขอบปุ่ม
    pygame.draw.rect(screen, WHITE, 
                   (button_x, button_y, button_width, button_height), 2)
    
    # ข้อความบนปุ่มพร้อมเอฟเฟกต์เรืองแสง
    start_font = pygame.font.SysFont('Arial', 30, bold=True)
    start_text = start_font.render("เริ่มเกม", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, button_y + button_height // 2))
    
    # เอฟเฟกต์เรืองแสงของข้อความ
    glow_text = start_font.render("เริ่มเกม", True, (255, 255, 200))
    glow_rect = glow_text.get_rect(center=(WIDTH // 2, button_y + button_height // 2))
    
    if pulse > 0:
        screen.blit(glow_text, (glow_rect.x, glow_rect.y))
    screen.blit(start_text, start_rect)
    
    # คำแนะนำพร้อมกล่องตกแต่ง
    instruction_bg = pygame.Surface((400, 80), pygame.SRCALPHA)
    instruction_bg.fill((0, 0, 0, 150))
    screen.blit(instruction_bg, (WIDTH // 2 - 200, button_y + button_height + 20))
    
    # คำแนะนำ
    instruction_font = pygame.font.SysFont('Arial', 18)
    instruction_text = instruction_font.render("คลิกปุ่มเพื่อเริ่มเล่น!", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, button_y + button_height + 40))
    screen.blit(instruction_text, instruction_rect)
    
    # คำแนะนำเพิ่มเติมเกี่ยวกับเมฆ
    cloud_text = instruction_font.render("ระวังเมฆที่เคลื่อนที่บังลูกธนูของคุณ!", True, WHITE)
    cloud_rect = cloud_text.get_rect(center=(WIDTH // 2, button_y + button_height + 70))
    screen.blit(cloud_text, cloud_rect)
    
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
    arrow_x, arrow_y = 100, HEIGHT // 2  # ตำแหน่งเริ่มต้นของลูกธนู
    angle = 0  # มุมการยิง
    shooting = False  # สถานะการยิง
    velocity = 0  # ความเร็วลูกธนู
    hit = False  # ตรวจสอบการโดน
    score = 0
    shots = 0

    # ตัวแปรการเปลี่ยนแรง
    base_velocity = 15
    force_variation = 0
    last_force_change_time = pygame.time.get_ticks()
    force_change_interval = 10000  # 10000ms = 10 นาที (สำหรับทดสอบ, จริงๆ 10 นาทีคือ 600000)
    
    # ตัวแปรเมฆ
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
            draw_archer(arrow_x - 30, arrow_y, angle)
            draw_instructions()

            # แสดงคะแนน
            score_text = font.render(f"คะแนน: {score} | จำนวนยิง: {shots}", True, BLACK)
            force_text = font.render(f"แรง: {base_velocity - force_variation} กม./ชม.", True, BLACK)
            screen.blit(score_text, (WIDTH - 200, 20))
            screen.blit(force_text, (WIDTH - 200, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        angle = min(angle + 5, 70)  # จำกัดมุมสูงสุด
                    elif event.key == pygame.K_DOWN:
                        angle = max(angle - 5, -20)  # จำกัดมุมต่ำสุด
                    elif event.key == pygame.K_SPACE and not shooting:
                        shooting = True
                        velocity = base_velocity - force_variation
                        shots += 1
                    elif event.key == pygame.K_ESCAPE:
                        # กลับสู่หน้าจอเริ่มต้น
                        in_start_screen = True
                        # รีเซ็ตตัวแปรเกม
                        arrow_x, arrow_y = 100, HEIGHT // 2
                        angle = 0
                        shooting = False
                        target_x = random.randint(600, 750)


            if shooting:
                arrow_x += velocity * math.cos(math.radians(angle))
                arrow_y -= velocity * math.sin(math.radians(angle))

                # เพิ่มผลของแรงโน้มถ่วงเพื่อให้สมจริง
                arrow_y += 0.5 * velocity * 0.1

                # ตรวจสอบการชนกับเมฆ
                cloud_collision = (
                    is_point_in_ellipse(arrow_x, arrow_y, cloud_x, cloud_y, cloud_width, cloud_height) or
                    is_point_in_ellipse(arrow_x, arrow_y, cloud_x - cloud_width/4, cloud_y + cloud_height/4, cloud_width/2, cloud_height/2) or
                    is_point_in_ellipse(arrow_x, arrow_y, cloud_x + cloud_width/2, cloud_y + cloud_height/4, cloud_width/2, cloud_height/2)
                )
                
                if cloud_collision:
                    shooting = False
                    arrow_x, arrow_y = 100, HEIGHT // 2
                    print("ลูกธนูชนเมฆ!")

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
                    arrow_x, arrow_y = 100, HEIGHT // 2
                elif arrow_x > WIDTH or arrow_y < 0 or arrow_y > HEIGHT:
                    shooting = False
                    arrow_x, arrow_y = 100, HEIGHT // 2

            # วาดรอยของลูกธนูขณะยิง
            if shooting:
                for i in range(1, 5):
                    trace_x = arrow_x - i * 8 * math.cos(math.radians(angle))
                    trace_y = arrow_y + i * 8 * math.sin(math.radians(angle))
                    pygame.draw.circle(screen, (200, 200, 200, 128), (int(trace_x), int(trace_y)), 2)

            # วาดลูกธนู
            rotated_arrow = pygame.transform.rotate(arrow_img, -angle)
            screen.blit(rotated_arrow, (arrow_x, arrow_y))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
