---
sidebar_position: 2
---

# ROS 2 Fundamentals

ROS 2 (Robot Operating System 2) is the industry-standard middleware framework for robotics applications. It provides tools, libraries, and conventions to create complex robot behavior across diverse hardware platforms.

## What is ROS 2?

ROS 2 is not an operating system in the traditional sense. It's a **middleware layer** that sits between your robot's hardware and your application code, providing:

- **Communication infrastructure** between different robot components
- **Hardware abstraction** so code works across different robots
- **Standard tools** for visualization, debugging, and data recording
- **Packaged libraries** for common robotics tasks

### Key Differences from ROS 1

ROS 2 brings significant improvements over the original ROS:

1. **Real-time capable** - Deterministic communication for safety-critical applications
2. **Security built-in** - DDS (Data Distribution Service) with encryption
3. **Multi-platform** - Windows, macOS, Linux, and embedded systems
4. **Better quality of service** - Configurable reliability and performance
5. **No master node** - Decentralized architecture for robustness

## Core Concepts

### Nodes

A **node** is a single computational process in the ROS graph. Nodes are the building blocks of ROS applications:

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_node')
        self.get_logger().info('Node has been started')

def main():
    rclpy.init()
    node = MinimalNode()
    rclpy.spin(node)
    rclpy.shutdown()
```

**Best Practices**:
- One node = one purpose (single responsibility principle)
- Name nodes descriptively (`camera_driver`, `obstacle_detector`)
- Keep nodes modular for reusability

### Topics

**Topics** are named buses for asynchronous message passing. Nodes publish messages to topics and subscribe to topics to receive messages:

```python
from std_msgs.msg import String

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.publisher = self.create_publisher(String, 'robot_status', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Robot is operational'
        self.publisher.publish(msg)
```

**When to use topics**:
- Continuous data streams (sensor readings)
- Broadcasting to multiple subscribers
- Fire-and-forget communication pattern

### Services

**Services** provide synchronous request-response communication:

```python
from example_interfaces.srv import AddTwoInts

class ServiceNode(Node):
    def __init__(self):
        super().__init__('service_node')
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints_callback
        )

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        return response
```

**When to use services**:
- Request-response patterns
- Infrequent operations
- When you need confirmation of completion

### Actions

**Actions** are for long-running tasks with feedback and cancellation:

```python
from action_tutorials_interfaces.action import Fibonacci
import rclpy.action

class ActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = rclpy.action.ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback
        )

    def execute_callback(self, goal_handle):
        # Implement long-running task with feedback
        pass
```

**When to use actions**:
- Long-running operations (navigation, grasping)
- Need periodic feedback
- Ability to cancel operations

## ROS 2 Workspace Structure

A typical ROS 2 workspace:

```
ros2_ws/
├── src/
│   ├── package_1/
│   │   ├── package_1/
│   │   │   ├── __init__.py
│   │   │   └── node_script.py
│   │   ├── package.xml
│   │   ├── setup.py
│   │   └── setup.cfg
│   └── package_2/
├── build/
├── install/
└── log/
```

### Creating a Package

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_robot_package
```

### Building the Workspace

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

## Essential ROS 2 Commands

### Node Management

```bash
# List running nodes
ros2 node list

# Get info about a node
ros2 node info /my_node

# Run a node
ros2 run package_name node_name
```

### Topic Operations

```bash
# List active topics
ros2 topic list

# Echo topic messages
ros2 topic echo /robot_status

# Publish to a topic
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "..."

# Get topic info
ros2 topic info /scan
```

### Service Operations

```bash
# List services
ros2 service list

# Call a service
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 1, b: 2}"
```

### Parameter Management

```bash
# List parameters
ros2 param list

# Get parameter value
ros2 param get /my_node my_parameter

# Set parameter
ros2 param set /my_node my_parameter value
```

## Quality of Service (QoS)

QoS profiles control message delivery behavior:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

qos = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,  # or BEST_EFFORT
    durability=DurabilityPolicy.TRANSIENT_LOCAL,  # or VOLATILE
    depth=10
)

self.publisher = self.create_publisher(String, 'topic', qos)
```

**Common profiles**:
- **Sensor data**: Best effort, volatile (fast, lossy OK)
- **Parameters**: Reliable, transient local (must deliver)
- **Commands**: Reliable, volatile (must deliver, don't need history)

## Launch Files

Launch files start multiple nodes with configuration:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_package',
            executable='my_node',
            name='my_node',
            parameters=[{'param1': 'value1'}]
        ),
        Node(
            package='another_package',
            executable='another_node',
            name='another_node'
        )
    ])
```

Run with:
```bash
ros2 launch my_package my_launch_file.launch.py
```

## Best Practices

1. **Naming Conventions**
   - Topics: lowercase with underscores (`/robot/sensor_data`)
   - Nodes: lowercase with underscores (`camera_driver`)
   - Namespaces: organize related nodes (`/robot1/`, `/robot2/`)

2. **Error Handling**
   - Always check service call results
   - Handle timeouts gracefully
   - Log errors appropriately

3. **Performance**
   - Choose appropriate QoS for your use case
   - Avoid large messages on high-frequency topics
   - Use composable nodes for efficiency

4. **Testing**
   - Write unit tests for node logic
   - Use `launch_testing` for integration tests
   - Test with various QoS settings

## Next Steps

Now that you understand ROS 2 fundamentals, you're ready to:
- Learn about robot simulation in Gazebo
- Explore sensor integration
- Build your first robot application

Continue to the next chapter to learn about simulation environments!