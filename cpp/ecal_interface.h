#ifndef ECALCPP_ECAL_INTERFACE_H
#define ECALCPP_ECAL_INTERFACE_H

#include <ecal/ecal.h>
#include <ecal/msg/protobuf/publisher.h>
#include <ecal/msg/protobuf/subscriber.h>
#include <iostream>
#include <string>
#include "image.pb.h"
#include <opencv2/core.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include "opencv2/imgproc/imgproc.hpp"

namespace eCALIO{
    template<typename T_topic>
    class InputInterface {
    private:
        const char* processName;
        const char* topicName;
        eCAL::protobuf::CSubscriber<T_topic> subscriber;

        void startProcess() {
            eCAL::Initialize(0, nullptr, processName);
            eCAL::Process::SetState(proc_sev_healthy, proc_sev_level1, " ");
        }

        void createSubscriber() {
            subscriber.Create(getTopicName());
        }

    public:
        T_topic message;

        explicit InputInterface(const char* topic = "ecal_input")
                : topicName{topic} {
            processName = "C++ Subscriber";
            startProcess();
            createSubscriber();
        }

        bool receiveMessage() {
            return subscriber.Receive(message);
        }

        std::string getProcessName() const {
            return processName;
        }

        std::string getTopicName() const {
            return topicName;
        }
    };
    template<typename T_topic>
    class OutputInterface {
    private:
        const char* processName;
        const char* topicName;
        bool messageWasSent;
        eCAL::protobuf::CPublisher<T_topic> publisher;

        void startProcess() {
            eCAL::Initialize(0, nullptr, processName);
            eCAL::Process::SetState(proc_sev_healthy, proc_sev_level1, " ");
        }

        void createPublisher() {
            publisher.Create(getTopicName());
        }

    public:
        T_topic message;

        explicit OutputInterface(const char* topic = "ecal_output")
                : topicName{topic} {
            processName = "C++ Publisher";
            messageWasSent = false;
            startProcess();
            createPublisher();
        }

        void sendMessage() {
            setMessageWasSent(publisher.Send(message));
        }

        std::string getProcessName() const {
            return processName;
        }

        std::string getTopicName() const {
            return topicName;
        }

        bool getMessageWasSent() const {
            return messageWasSent;
        }

        void setMessageWasSent(bool value) {
            messageWasSent = value;
        }
    };

    class ImageOutput : public OutputInterface<pb::image> {

    public:
        ImageOutput()
                : OutputInterface("image") {}

        void updateMessage(cv::Mat const &image, pb::compression compression, pb::colorspace color) {

            cv::uint8_t vectorizedImage[640 * 480 * 3];
            int idx = 0;
            for(int col=0; col<image.cols; col++){
                for(int row=0; row<image.rows; row++){
                    vectorizedImage[idx++] = image.at<cv::Vec3b>(row,col)[0];
                    vectorizedImage[idx++] = image.at<cv::Vec3b>(row,col)[1];
                    vectorizedImage[idx++] = image.at<cv::Vec3b>(row,col)[2];
                }
            }
            message.set_height(image.cols);
            message.set_width(image.rows);
            message.set_channels(image.channels());
            message.set_imagecompression(compression);
            message.set_color(color);
            message.set_data(&vectorizedImage, image.rows * image.cols * 3);
        }
    };

} // namespace eCALIO

#endif //ECALCPP_ECAL_INTERFACE_H
