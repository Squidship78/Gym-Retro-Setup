import time

import numpy as np
import retro
from gym.utils.play import play
import pygame as pg
import csv

# w,h = 800,800
# screen = pg.display.set_mode([w,h])

# def array2suf(arr):
#     return pg.surfarray.make_surface(arr)


def array_to_surface(array):
    """Convert a numpy.ndarray to a pygame.Surface without transposing."""
    return pg.surfarray.make_surface(array)

# def main():
#
#     clock = pg.time.Clock()
#     # env = retro.make(game="Gravitar")
#     env = retro.make(game="Asteroids")
#     env.reset()
#     asteroids_action_key_map = {
#         pg.K_j: 0,  # j 射击
#         pg.K_w: 4,  # w 前进
#         pg.K_a: 6,  # a 左旋转
#         pg.K_d: 7,  # d 右旋转
#     }
#     gravitar_action_key_map = {
#         pg.K_j:0,#j 射击
#         pg.K_w:4,#w 前进
#         pg.K_a:6,#a 左旋转
#         pg.K_d:7,#d 右旋转
#     }
#     if env.gamename=="Asteroids":
#         action_key_map = asteroids_action_key_map
#     elif env.gamename=="Gravitar":
#         action_key_map=gravitar_action_key_map
#     while True:
#         for ev in pg.event.get():
#             pass
#         action = [0 for _ in range(env.num_buttons)]
#         for k,v in action_key_map.items():
#             if pg.key.get_pressed()[k]:
#                 action[v]=1
#         data = env.step(action)
#         # print(data)
#
#         im = pg.transform.scale(pg.transform.flip(pg.transform.rotate(array2suf(env.render(mode="rgb_array")),-90),True,False),[w,h])
#         screen.blit(im,[0,0])
#         pg.display.update()
#         clock.tick(60)
def main():
    pg.init()
    w, h = 1024, 768  # Define screen width and height
    screen = pg.display.set_mode((w, h))
    clock = pg.time.Clock()

    env = retro.make(game="Asteroids")
    env.reset()

    # User input for unique filename or ID
    user_id = input("Enter your user ID or name: ")
    directory = "C:\workspace\Data"  # Specify your desired directory here
    filename = f"{directory}/{user_id}_scores.csv"

    asteroids_action_key_map = {
        pg.K_j: 0,  # j Shoot
        pg.K_w: 4,  # w Forward
        pg.K_a: 6,  # a Rotate Left
        pg.K_d: 7,  # d Rotate Right
    }

    action_key_map = asteroids_action_key_map  # Assuming only one game for simplification

    lives = 4  # Starting lives
    game_over = False

    start_time = time.time()
    last_score = 0  # Track the last known score

    pg.display.set_mode((w, h))

    # Open or create a CSV file for the current user
    with open(filename, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Score", "Time Taken"])  # Write header if creating a new file

        while not game_over:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    game_over = True

            action = [0 for _ in range(env.num_buttons)]
            for k, v in action_key_map.items():
                if pg.key.get_pressed()[k]:
                    action[v] = 1

            obs, reward, done, info = env.step(action)

            if done or info.get('lives', 0) < lives:
                game_over = True  # End the game if done or lives decreased

            score = info.get('score', 0)  # Adjust key if necessary

            if score != last_score:  # Check if the score has changed
                current_time = time.time() - start_time
                csvwriter.writerow([score * 10, f"{current_time:.2f}"])  # Write score and time to CSV
                last_score = score  # Update the last known score

            im_array = env.render(mode="rgb_array")  # Assuming this is the correct call for your retro version
            im_surface = array_to_surface(im_array)
            im_transformed = pg.transform.scale(pg.transform.flip(pg.transform.rotate(im_surface, 90), False, True),
                                                (w, h))
            screen.blit(im_transformed, (0, 0))

            # im = pg.transform.scale(pg.transform.flip(pg.transform.rotate(array_to_surface(env.render(mode="rgb_array")),-90),True,False),[w,h])
            # screen.blit(im,[0,0])


            pg.display.update()
            clock.tick(60)

        end_time = time.time()
        time_taken = end_time - start_time
        final_score = score * 10
        print(f"Final Score: {final_score}, Time Taken: {time_taken:.2f} seconds")
        csvwriter.writerow(["Final Score", "Final Time Taken"])
        csvwriter.writerow([final_score, f"{time_taken:.2f}"])  # Record final score and time

    env.close()
    pg.quit()


if __name__ == "__main__":
    main()


# with open("data.csv", mode="w", newline="") as file:
#      writer = csv. writer(file)
#      writer.writerows(data)