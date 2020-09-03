#!/usr/bin/python
#
# Made from:
# https://arcade.academy/examples/platform_tutorial/index.html

import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
PLAYER_SCALE = 1
TILE_SCALE = 0.5

PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20
GRAVITY = 0.5

LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100

class MyGame(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Platformer")

        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        self.player_sprite = None

        self.physics_engine = None

        self.view_bottom = 0
        self.view_left = 0

        self.score = 0

        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = arcade.Sprite(
            ":resources:images/animated_characters/male_person/malePerson_idle.png", PLAYER_SCALE)
        self.player_sprite.center_x = 0
        self.player_sprite.center_y = 120
        self.player_list.append(self.player_sprite)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:/images/tiles/grassMid.png", TILE_SCALE)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        coordinate_list = [[512, 96],
                           [256, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            crate = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALE)
            crate.position = coordinate
            self.wall_list.append(crate)

        for x in range(128, 1250, 256):
            coin = arcade.Sprite(":resources:images/items/coinGold.png")
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)
    
    def on_update(self, delta_time):

        self.physics_engine.update()

        coin_hit_list = set(arcade.check_for_collision_with_list(self.player_sprite, self.coin_list))

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.collect_coin_sound)

        # Viewport
        changed = False

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN

        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True
        if self.player_sprite.right > right_boundary:
            self.view_left +=  self.player_sprite.right - right_boundary
            changed = True
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def on_draw(self):
        arcade.start_render()

        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP and self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
            arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
