import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from std_msgs.msg import String


class MinimalSubscriber1(Node):

    def __init__(self):
        super().__init__('minimal_subscriber1')
        self.subscription1 = self.create_subscription(
            String,
            'topic1',
            self.listener_callback1,
            10)
        self.subscription1  # prevent unused variable warning

    def listener_callback1(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

class MinimalSubscriber2(Node):

    def __init__(self):
        super().__init__('minimal_subscriber2')
        self.subscription2 = self.create_subscription(
            String,
            'topic2',
            self.listener_callback2,
            10)
        self.subscription2  # prevent unused variable warning

    def listener_callback2(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    


    try:
        minimal_subscriber1 = MinimalSubscriber1()
        minimal_subscriber2 = MinimalSubscriber2()

        # MultiThreadedExecutor executes callbacks with a thread pool. If num_threads is not
        # specified then num_threads will be multiprocessing.cpu_count() if it is implemented.
        # Otherwise it will use a single thread. This executor will allow callbacks to happen in
        # parallel, however the MutuallyExclusiveCallbackGroup in DoubleTalker will only allow its
        # callbacks to be executed one at a time. The callbacks in Listener are free to execute in
        # parallel to the ones in DoubleTalker however.
        executor = MultiThreadedExecutor(num_threads=4)
        executor.add_node( minimal_subscriber1)
        executor.add_node( minimal_subscriber2)
        try:
            executor.spin()
        finally:
            executor.shutdown()
            minimal_subscriber1.destroy_node()
            minimal_subscriber2.destroy_node()
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()
