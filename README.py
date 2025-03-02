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
    """Draw the game background with sky, mountains, and grass."""
    # Sky gradient
    for y in range(HEIGHT):
        # Create a sky gradient from deep blue to light blue
        depth = 1 - (y / HEIGHT * 0.7)
        sky_color = (int(135 * depth), int(206 * depth), int(235 * depth))
        pygame.draw.line(screen, sky_color, (0, y), (WIDTH, y))
    
    # Mountains in the background
    mountain_color = (100, 100, 100)
    mountain_points = [(0, HEIGHT-150), (WIDTH/4, HEIGHT-250), 
                       (WIDTH/2, HEIGHT-200), (WIDTH*3/4, HEIGHT-280), 
                       (WIDTH, HEIGHT-180), (WIDTH, HEIGHT-100), (0, HEIGHT-100)]
    pygame.draw.polygon(screen, mountain_color, mountain_points)
    
    # Sun with rays
    sun_x, sun_y = WIDTH - 100, 100
    # Main sun
    pygame.draw.circle(screen, GOLDEN, (sun_x, sun_y), 40)
    # Sun glow
    for radius in range(45, 60, 5):
        pygame.draw.circle(screen, (255, 215, 0, 100-radius), (sun_x, sun_y), radius, 2)
    
    # Draw sun rays
    for angle in range(0, 360, 30):
        end_x = sun_x + math.cos(math.radians(angle)) * 60
        end_y = sun_y + math.sin(math.radians(angle)) * 60
        pygame.draw.line(screen, GOLDEN, (sun_x, sun_y), (end_x, end_y), 2)
    
    # Grass with texture
    pygame.draw.rect(screen, GRASS_GREEN, (0, HEIGHT - 100, WIDTH, 100))
    # Add grass details
    for i in range(0, WIDTH, 20):
        grass_height = random.randint(5, 15)
        pygame.draw.line(screen, (45, 160, 45), (i, HEIGHT - 100), (i, HEIGHT - 100 - grass_height), 2)

def draw_archer(x, y, angle):
    """Draw a more detailed archer figure."""
    # Body
    body_color = (80, 60, 40)
    pygame.draw.line(screen, body_color, (x - 30, y), (x - 30, y + 40), 5)
    
    # Head
    head_color = (210, 180, 140)
    pygame.draw.circle(screen, head_color, (x - 30, y - 10), 8)
    
    # Arms
    pygame.draw.line(screen, body_color, (x - 30, y + 10), (x - 5, y), 4)
    pygame.draw.line(screen, body_color, (x - 30, y + 10), (x - 10, y + 15), 4)
    
    # Legs
    pygame.draw.line(screen, body_color, (x - 30, y + 40), (x - 35, y + 55), 4)
    pygame.draw.line(screen, body_color, (x - 30, y + 40), (x - 25, y + 55), 4)
    
    # Bow
    bow_radius = 30
    bow_color = (139, 69, 19)
    bow_string_color = (255, 255, 240)
    bow_start_angle = math.radians(angle - 30)
    bow_end_angle = math.radians(angle + 30)
    
    # Draw bow (thicker with multiple lines)
    for i in range(5):
        offset = i - 2
        pygame.draw.arc(screen, bow_color, 
                        (x - bow_radius + offset, y - bow_radius + offset, 
                         bow_radius * 2, bow_radius * 2),
                        bow_start_angle, bow_end_angle, 2)
    
    # Draw bowstring
    string_start_x = x + bow_radius * 0.85 * math.cos(bow_start_angle)
    string_start_y = y + bow_radius * 0.85 * math.sin(bow_start_angle)
    string_end_x = x + bow_radius * 0.85 * math.cos(bow_end_angle)
    string_end_y = y + bow_radius * 0.85 * math.sin(bow_end_angle)
    pygame.draw.line(screen, bow_string_color, (string_start_x, string_start_y), (string_end_x, string_end_y), 1)

def draw_target(target_x, target_y, target_radius):
    """Draw a detailed target with wooden stand."""
    # Target stand
    stand_width = 20
    stand_color = DARK_BROWN
    stand_light_color = LIGHT_BROWN
    
    # Wooden stand with texture
    pygame.draw.rect(screen, stand_color, (target_x - stand_width/2, target_y, stand_width, HEIGHT - target_y - 100))
    
    # Add wood grain
    for i in range(5):
        y_pos = target_y + i * 30
        if y_pos < HEIGHT - 100:
            pygame.draw.line(screen, stand_light_color, 
                            (target_x - stand_width/2, y_pos), 
                            (target_x + stand_width/2, y_pos), 1)
    
    # Shadow under the target
    shadow_color = (0, 0, 0, 50)  # Semi-transparent black
    pygame.draw.ellipse(screen, (70, 40, 0), (target_x - target_radius, target_y + target_radius*0.9, target_radius*2, target_radius*0.3))
    
    # Target rings with 3D effect
    for radius, color in target_rings:
        pygame.draw.circle(screen, color, (target_x, target_y), radius)
        # Add a highlight effect for 3D appearance
        if radius > target_radius * 0.2:  # Don't add highlight to bullseye
            pygame.draw.arc(screen, (255, 255, 255, 100), 
                          (target_x - radius, target_y - radius, radius*2, radius*2),
                          math.radians(45), math.radians(135), 2)

def calculate_distance(x1, y1, x2, y2):
    """Calculate the distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def is_point_in_ellipse(x, y, ellipse_x, ellipse_y, width, height):
    """Check if a point is inside an ellipse."""
    # Adjust coordinates to ellipse center
    nx = x - (ellipse_x + width/2)
    ny = y - (ellipse_y + height/2)
    
    # Check if point is inside the ellipse
    return (nx**2 / (width/2)**2) + (ny**2 / (height/2)**2) <= 1

def draw_cloud(x, y, width, height):
    """Draw a fluffy cloud with gradient and detail."""
    # Cloud layers for more realism
    cloud_layers = [
        (0, 0, width, height),
        (-width/4, height/4, width/2, height/2),
        (width/2, height/4, width/2, height/2),
        (width/4, -height/5, width/2, height/2),
        (width/10, height/3, width/3, height/3)
    ]
    
    # Draw cloud core with gradient
    for layer in cloud_layers:
        base_x, base_y, layer_width, layer_height = layer
        for i in range(4):  # Multiple layers for gradient effect
            opacity = 220 - i * 20
            cloud_shade = (min(255, CLOUD_COLOR[0] - i*5), 
                           min(255, CLOUD_COLOR[1] - i*5), 
                           min(255, CLOUD_COLOR[2] - i*5))
            pygame.draw.ellipse(screen, cloud_shade,
                              (x + base_x, y + base_y, layer_width, layer_height))
    
    # Add highlight to give clouds volume
    highlight_color = (250, 250, 250)
    pygame.draw.ellipse(screen, highlight_color,
                      (x + width/8, y + height/8, width/4, height/4))
    
    # Subtle border for definition
    border_color = (220, 220, 220)
    for layer in cloud_layers:
        base_x, base_y, layer_width, layer_height = layer
        pygame.draw.ellipse(screen, border_color,
                          (x + base_x, y + base_y, layer_width, layer_height), 1)

def draw_instructions():
    """Draw game instructions with styled box."""
    # Draw a semi-transparent background for instructions
    instruction_bg = pygame.Surface((200, 110), pygame.SRCALPHA)
    instruction_bg.fill((0, 0, 0, 100))  # Semi-transparent black
    screen.blit(instruction_bg, (10, 10))
    
    # Add a border
    pygame.draw.rect(screen, WHITE, (10, 10, 200, 110), 1)
    
    # Title
    title_font = pygame.font.SysFont('Arial', 20, bold=True)
    title_surf = title_font.render("CONTROLS:", True, WHITE)
    screen.blit(title_surf, (20, 15))
    
    # Instructions with icons
    instructions = [
        "↑/↓: ปรับมุมยิง",
        "SPACE: ยิงลูกธนู",
        "ESC: กลับสู่เมนูหลัก"
    ]

    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (20, 45 + i * 25))

def draw_start_screen():
    """Draw an animated and detailed start screen."""
    # Background with gradient sky
    for y in range(HEIGHT):
        depth = 1 - (y / HEIGHT * 0.8)
        sky_color = (int(135 * depth), int(206 * depth), int(235 * depth))
        pygame.draw.line(screen, sky_color, (0, y), (WIDTH, y))
    
    # Moving clouds in background (decorative)
    time_offset = pygame.time.get_ticks() / 1000
    for i in range(3):
        cloud_x = ((time_offset * 20) + i * WIDTH/3) % (WIDTH + 200) - 100
        cloud_y = HEIGHT/8 + i * HEIGHT/10
        draw_cloud(cloud_x, cloud_y, 120, 60)
    
    # Sun with rays
    pygame.draw.circle(screen, GOLDEN, (WIDTH - 100, 100), 40)
    for angle in range(0, 360, 30):
        end_x = WIDTH - 100 + math.cos(math.radians(angle)) * 60
        end_y = 100 + math.sin(math.radians(angle)) * 60
        pygame.draw.line(screen, GOLDEN, (WIDTH - 100, 100), (end_x, end_y), 2)
    
    # Grass with texture
    pygame.draw.rect(screen, GRASS_GREEN, (0, HEIGHT - 100, WIDTH, 100))
    # Add grass details
    for i in range(0, WIDTH, 10):
        grass_height = random.randint(5, 15)
        grass_x_offset = math.sin(time_offset + i/50) * 3  # Gentle wave effect
        pygame.draw.line(screen, (45, 160, 45), 
                       (i + grass_x_offset, HEIGHT - 100), 
                       (i, HEIGHT - 100 - grass_height), 2)
    
    # Game title with shadow effect
    title_font = pygame.font.SysFont('Arial', 70, bold=True)
    shadow_text = title_font.render("ARCHERY CHALLENGE", True, (50, 30, 10))
    title_text = title_font.render("ARCHERY CHALLENGE", True, DARK_BROWN)
    
    screen.blit(shadow_text, (WIDTH // 2 - shadow_text.get_width() // 2 + 4, HEIGHT // 3 + 4))
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    
    # Draw bow and arrow icon with animation
    bow_x, bow_y = WIDTH // 2, HEIGHT // 2 - 30
    time_val = pygame.time.get_ticks() / 1000  # For animation
    bow_pull = abs(math.sin(time_val * 2)) * 10  # Animated bow pull
    
    # Bow with animation
    pygame.draw.arc(screen, BROWN, 
                  (bow_x - 50, bow_y - 50, 100, 100),
                  math.radians(-30), math.radians(30), 4)
    
    # Bowstring with animation
    string_start_x = bow_x - 40 + bow_pull
    string_end_x = bow_x + 40 - bow_pull
    pygame.draw.line(screen, WHITE, (string_start_x, bow_y - 30), (bow_x, bow_y), 2)
    pygame.draw.line(screen, WHITE, (string_end_x, bow_y - 30), (bow_x, bow_y), 2)
    
    # Arrow
    pygame.draw.line(screen, DARK_BROWN, (bow_x - 40 + bow_pull, bow_y), (bow_x + 40, bow_y), 3)
    
    # Arrow tip
    pygame.draw.polygon(screen, DARK_RED, [(bow_x + 40, bow_y),
                                         (bow_x + 50, bow_y - 5),
                                         (bow_x + 50, bow_y + 5)])
    
    # Start button with pulsing effect
    button_width, button_height = 200, 60
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT * 3 // 4
    
    # Button pulse animation
    pulse = math.sin(time_val * 4) * 5
    button_glow = max(0, int(pulse * 20))
    
    # Button with shadow
    pygame.draw.rect(screen, (100, 0, 0), 
                   (button_x - 5, button_y - 3, button_width + 10, button_height + 6))
    
    # Main button
    pygame.draw.rect(screen, (DARK_RED[0] + button_glow, DARK_RED[1], DARK_RED[2]),
                   (button_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, (RED[0] + button_glow, RED[1], RED[2]),
                   (button_x + 4, button_y + 4, button_width - 8, button_height - 8))
    
    # Button border
    pygame.draw.rect(screen, WHITE, 
                   (button_x, button_y, button_width, button_height), 2)
    
    # Button text with glow
    start_font = pygame.font.SysFont('Arial', 30, bold=True)
    start_text = start_font.render("START GAME", True, WHITE)
    start_rect = start_text.get_rect(center=(WIDTH // 2, button_y + button_height // 2))
    
    # Text glow effect
    glow_text = start_font.render("START GAME", True, (255, 255, 200))
    glow_rect = glow_text.get_rect(center=(WIDTH // 2, button_y + button_height // 2))
    
    if pulse > 0:
        screen.blit(glow_text, (glow_rect.x, glow_rect.y))
    screen.blit(start_text, start_rect)
    
    # Instructions with decorative box
    instruction_bg = pygame.Surface((400, 80), pygame.SRCALPHA)
    instruction_bg.fill((0, 0, 0, 150))
    screen.blit(instruction_bg, (WIDTH // 2 - 200, button_y + button_height + 20))
    
    # Instructions
    instruction_font = pygame.font.SysFont('Arial', 18)
    instruction_text = instruction_font.render("คลิกปุ่มเพื่อเริ่มเล่น!", True, WHITE)
    instruction_rect = instruction_text.get_rect(center=(WIDTH // 2, button_y + button_height + 40))
    screen.blit(instruction_text, instruction_rect)
    
    # Additional instruction about cloud
    cloud_text = instruction_font.render("ระวังเมฆที่เคลื่อนที่บังลูกธนูของคุณ!", True, WHITE)
    cloud_rect = cloud_text.get_rect(center=(WIDTH // 2, button_y + button_height + 70))
    screen.blit(cloud_text, cloud_rect)
    
    # Add decorative targets in background
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
                    mouse_x, mouse_y = pygame.mouse.get_pos()จ
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
