from launch import LaunchDescription
from launch_ros.actions import Node
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        
        Node(
            package='camera_package',
            executable='camera_streamer',
            name='camera_streamer',
            output='screen',
        ),

        Node(
            package='camera_package',
            executable='camera_opencv_loop',
            name='camera_opencv_loop',
            output='screen',
        ),

    ])
