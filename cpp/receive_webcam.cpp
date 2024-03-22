#include <iostream>
#include <string>
#include "image.pb.h"
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include "opencv2/imgproc/imgproc.hpp"
#include <ecal/ecal.h>
#include <ecal/msg/protobuf/subscriber.h>


int main(int argc, char *argv[])
{
    // Subscribers names
    const char *topic_mi_mensaje = "image";

    // Creating Process
    eCAL::Initialize(argc, argv, "C++ Subscriber");
    eCAL::Process::SetState(proc_sev_healthy, proc_sev_level1, " ");
    // Creating subscribers and its message
    eCAL::protobuf::CSubscriber<pb::image> sub_mensaje(topic_mi_mensaje);
    pb::image protobuf_message;

    eCAL::Process::SleepMS(1000);

    cv::Mat frame, frame_gray;

    bool isReceived = false;
    for (;;)
    {
        isReceived = sub_mensaje.Receive(protobuf_message, nullptr, 100);

        if (isReceived) {
            std::cout << protobuf_message.name() << "\n";
            frame.create(protobuf_message.height(),
                         protobuf_message.width(),
                         16);
            auto data = reinterpret_cast<unsigned char const*>(protobuf_message.data().data());
            std::copy(data, (data + (frame.rows * frame.cols * 3)), frame.data);

        cv::imshow("Received image", frame);
        }

        eCAL::Process::SleepMS(5);
        if (cv::waitKey(5) >= 0)
            break;
    }
    return 0;
}