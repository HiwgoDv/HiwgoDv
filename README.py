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

# โหลดภาพลูกธนู
arrow_img = pygame.image.load("arrow.png")
arrow_img = pygame.transform.scale(arrow_img, (40, 10))

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
    """วาดพื้นหลังของเกมที่มีท้องฟ้าและหญ้า"""
    # ท้องฟ้า
    screen.fill(SKY_BLUE)
    # หญ้า
    pygame.draw.rect(screen, GRASS_GREEN, (0, HEIGHT - 100, WIDTH, 100))
    # พระอาทิตย์
    pygame.draw.circle(screen, GOLDEN, (WIDTH - 100, 100), 40)

def draw_archer(x, y, angle):
    """วาดนักธนูที่มีลักษณะพื้นฐาน"""
    # ลำตัว
    pygame.draw.line(screen, DARK_BROWN, (x - 30, y), (x - 30, y + 30), 3)
    # แขนที่ถือธนู
    pygame.draw.line(screen, DARK_BROWN, (x - 30, y + 10), (x, y), 3)
    # ธนู
    bow_height = 40
    bow_radius = 30
    bow_start_angle = math.radians(angle - 30)
    bow_end_angle = math.radians(angle + 30)

    for i in range(5):  # วาดธนูให้หนาขึ้นโดยใช้หลายเส้น
        offset = i - 2
        pygame.draw.arc(screen, BROWN, 
                        (x - bow_radius + offset, y - bow_radius + offset, 
                         bow_radius * 2, bow_radius * 2),
                        bow_start_angle, bow_end_angle, 2)

def draw_target(target_x, target_y, target_radius):
    """วาดเป้าที่มีวงกลมซ้อนกัน"""
    for radius, color in target_rings:
        pygame.draw.circle(screen, color, (target_x, target_y), radius)

    # ขาตั้งเป้า
    pygame.draw.rect(screen, DARK_BROWN, (target_x - 5, target_y, 10, HEIGHT - target_y - 100))

def calculate_distance(x1, y1, x2, y2):
    """คำนวณระยะห่างระหว่างจุดสองจุด"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def is_point_in_ellipse(x, y, ellipse_x, ellipse_y, width, height):
    """ตรวจสอบว่าจุดอยู่ภายในวงรีหรือไม่"""
    # ปรับพิกัดให้ตรงกับศูนย์กลางของวงรี
    nx = x - (ellipse_x + width/2)
    ny = y - (ellipse_y + height/2)
    
    # ตรวจสอบว่าจุดอยู่ภายในวงรี
    return (nx**2 / (width/2)**2) + (ny**2 / (height/2)**2) <= 1

def draw_cloud(x, y, width, height):
    """วาดเมฆที่ปิดบังการยิง"""
    # วาดเมฆหลัก
    pygame.draw.ellipse(screen, CLOUD_COLOR, (x, y, width, height))
    # วาดก้อนเมฆเล็กๆ
    pygame.draw.ellipse(screen, CLOUD_COLOR, (x - width/4, y + height/4, width/2, height/2))
    pygame.draw.ellipse(screen, CLOUD_COLOR, (x + width/2, y + height/4, width/2, height/2))
    # เพิ่มขอบที่สีดำเบาๆ
    pygame.draw.ellipse(screen, (200, 200, 200), (x, y, width, height), 1)

def draw_instructions():
    """วาดคำแนะนำในการเล่นเกมบนหน้าจอ"""
    instructions = [
        "UP/DOWN: ปรับมุมยิง",
        "SPACE: ยิงลูกธนู",
        "ESC: กลับสู่เมนูหลัก"
    ]

    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (20, 20 + i * 30))

def draw_start_screen():
    """วาดหน้าจอเริ่มต้นที่มีชื่อเกมและปุ่มเริ่มเกม"""
    # เติมพื้นหลัง
    screen.fill(SKY_BLUE)

    # วาดองค์ประกอบตกแต่ง
    # พระอาทิตย์
    pygame.draw.circle(screen, GOLDEN, (WIDTH - 100, 100), 40)

    # หญ้า
    pygame.draw.rect(screen, GRASS_GREEN, (0, HEIGHT - 100, WIDTH, 100))

    # ชื่อเกม
    title_font = pygame.font.SysFont('Arial', 60, bold=True)
    title_text = title_font.render("ARCHERY CHALLENGE", True, DARK_BROWN)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title_text, title_rect)

    # วาดไอคอนธนูและลูกธนู
    bow_x, bow_y = WIDTH // 2, HEIGHT // 2 - 30
    # ธนู
    pygame.draw.arc(screen, BROWN, 
                    (bow_x - 50, bow_y - 50, 100, 100),
                    math.radians(-30), math.radians(30), 4)
    # ลูกธนู
    pygame.draw.line(screen, DARK_BROWN, (bow_x - 40, bow_y), (bow_x + 40, bow_y), 3)
    # ปลายลูกธนู
    pygame.draw.polygon(screen, DARK_RED, [(bow_x + 40, bow_y), 
                                          (bow_x + 50, bow_y - 5), 
                                          (bow_x + 50, bow_y + 5)])

    # ปุ่มเริ่มเกม
    button_width, button_height = 200, 50
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT * 3 // 4
    pygame.draw.rect(screen, DARK_RED, (button_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, RED, (button_x + 3, button_y + 3, button_width - 6, button_height - 6))

    # ข้อความเริ่มเกม
    start_font = pygame.font.SysFont('Arial', 30, bold=True)
    start_text = start_font.render("START GAME", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, button_y + button_height // 2))
    screen.blit(start_text, start_rect)

    # คำแนะนำ
    instruction_font = pygame.font.SysFont('Arial', 18)
    instruction_text = instruction_font.render("คลิกปุ่มเพื่อเริ่มเล่น!", True, BLACK)
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, button_y + button_height + 30))
    screen.blit(instruction_text, instruction_rect)
    
    # คำแนะนำเกี่ยวกับเมฆ
    cloud_text = instruction_font.render("ระวังเมฆที่เคลื่อนที่บังลูกธนูของคุณ!", True, BLACK)
    cloud_rect = cloud_text.get_rect(center=(WIDTH // 2, button_y + button_height + 55))
    screen.blit(cloud_text, cloud_rect)

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
            score_text = font.render(f"Score: {score} | Shots: {shots}", True, BLACK)
            force_text = font.render(f"Force: {base_velocity - force_variation} km/h", True, BLACK)
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
