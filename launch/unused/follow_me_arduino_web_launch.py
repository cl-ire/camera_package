from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        
        Node(
            package='camera_package',
            executable='camera_opencv_loop',
            name='camera_opencv_loop2',
            output='screen',
            parameters=[
                {'detector_type': "haarcascade"},
                {'timer_period': 0.5},
            ]
        ),
        Node(
            package='camera_package',
            executable='movement_control',
            name='movement_control',
            output='screen',
            parameters=[
                {'camera_max_winkel_x': 85},
                {'camera_max_winkel_y': 50},
                {'distance_to_person': 200},
                {'hight_of_person': 170},
                {'motor_settings_radius': 25},
                {'motor_settings_wheel_distance': 11},
                {'motor_settings_wheel_radius': 3.5},
                {'motor_settings_correction_factor': 1},
                {'motor_settings_base_rpm': 100},
                {'enable_movement': True},
            ]
        ),
        Node(
            package='camera_package',
            executable='web_control_center',
            name='web_control_center',
            output='screen',
        ),
        Node(
            package='camera_package',
            executable='arduino_interface',
            name='arduino_interface',
            output='screen',
        ),

    ])
