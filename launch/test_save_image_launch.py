from launch import LaunchDescription
from launch_ros.actions import Node
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        
        Node(
            package='camera_package',
            executable='camera_save_image',
            name='camera_save_image',
            output='screen',
            parameters=[
                {'path': "/home/ubuntu/image/"},
            ]
        ),

        Node(
            package='camera_package',
            executable='camera_opencv_loop',
            name='camera_opencv_loop',
            output='screen',
            parameters=[
                {'detector_type': "none"},
                {'timer_period': 0.5},
            ]
        ),

    ])
