// This autogenerated skeleton file illustrates how to build a server.
// You should copy it to another filename to avoid overwriting it.

#include "match_server/Match.h"
#include "message_client/Message.h"
#include <thrift/concurrency/ThreadManager.h>
#include <thrift/concurrency/ThreadFactory.h>
#include <thrift/server/TThreadPoolServer.h>
#include <thrift/server/TThreadedServer.h>
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TTransportUtils.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>
#include <thrift/TToString.h>

#include <iostream>
#include <cmath>
#include <jsoncpp/json/json.h>
#include <unistd.h>
#include "thread"
#include "mutex"
#include "condition_variable"
#include "queue"
#include "vector"

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;

using namespace  ::match_service;
using namespace std;

struct Task {
    Player player;
    string type;
};

struct MessageQueue {
    queue<Task> q;
    mutex m;
    condition_variable cv;
} message_queue;

class Pool {
    private:
        vector<Player> players;
        vector<int> wt;     // 等待时间, 单位: s

    public:
        void add(Player player) {
            players.push_back(player);
            wt.push_back(0);
        }

        void remove(Player player) {
            for(uint32_t i = 0; i < players.size(); i++) {
                if(players[i].id == player.id) {
                    players.erase(players.begin() + i);
                    wt.erase(wt.begin() + i);
                    break;
                }
            }
        }

        bool check_match(uint32_t i, uint32_t j) {
            auto playerA = players[i], playerB = players[j];

            int dt = abs(playerA.rating - playerB.rating);
            // min: 若取min则代表两者分差都小于 等待时间 * 10，实力差距最接近
            // max: 若取max则代表有一方分差小于 等待时间 * 10，实力差距可能会大
            int waitingtime = wt[i] < wt[j] ? wt[i] : wt[j];
            return dt <= waitingtime * 10;
        }

        void match() {
            for(uint32_t i = 0; i < wt.size(); i++) wt[i]++;

            while(players.size() > 1) {
                bool flag = true;
                for(uint32_t i = 0; i < players.size(); i++) {
                    for(uint32_t j = i + 1; j < players.size(); j++) {
                        if(check_match(i, j)) {
                            auto playerA = players[i], playerB = players[j];
                            players.erase(players.begin() + j);
                            players.erase(players.begin() + i);
                            wt.erase(wt.begin() + j);
                            wt.erase(wt.begin() + i);
                            save_result(playerA, playerB);
                            flag = false;
                            break;
                        }
                    }
                    if(!flag) break;
                }
                if(flag) break;
            }
        }

        void save_result(Player player1, Player player2) {
            std::shared_ptr<TTransport> socket(new TSocket("120.76.157.21", 9091));
            std::shared_ptr<TTransport> transport(new TBufferedTransport(socket));
            std::shared_ptr<TProtocol> protocol(new TBinaryProtocol(transport));
            MessageClient client(protocol);

            try {
                transport->open();

                Json::Value root, player;
                root["type"] = Json::Value("match");
                player["id"] = Json::Value(player1.id);
                player["username"] = Json::Value(player1.username);
                player["photo"] = Json::Value(player1.photo);
                player["channel_name"] = Json::Value(player1.channel_name);
                player["operate"] = Json::Value(player1.operate);
                player["bot_id"] = Json::Value(player1.bot_id);
                root["players"].append(player);

                player["id"] = Json::Value(player2.id);
                player["username"] = Json::Value(player2.username);
                player["photo"] = Json::Value(player2.photo);
                player["channel_name"] = Json::Value(player2.channel_name);
                player["operate"] = Json::Value(player2.operate);
                player["bot_id"] = Json::Value(player2.bot_id);
                root["players"].append(player);

                string resp = Json::FastWriter().write(root);
                client.response(resp);

                transport->close();
            } catch (TException& tx) {
                cout << "ERROR: " << tx.what() << endl;
            }
        }
} pool;

class MatchHandler : virtual public MatchIf {
    public:
        MatchHandler() {
            // Your initialization goes here
        }

        int32_t add_player(const Player& player, const std::string& info) {
            // Your implementation goes here
            printf("add_player\n");
            unique_lock<mutex> lock1(message_queue.m);
            message_queue.q.push({player, "add"});
            message_queue.cv.notify_all();

            return 0;
        }

        int32_t remove_player(const Player& player, const std::string& info) {
            // Your implementation goes here
            printf("remove_player\n");
            unique_lock<mutex> lock1(message_queue.m);
            message_queue.q.push({player, "remove"});
            message_queue.cv.notify_all();

            return 0;
        }

};

void consume_task() {
    while(true) {
        unique_lock<mutex> lock1(message_queue.m);
        if(message_queue.q.empty()) {
            lock1.unlock();
            pool.match();
            sleep(1);
        } else {
            auto task = message_queue.q.front();
            message_queue.q.pop();
            lock1.unlock();
            if(task.type == "add") {
                pool.add(task.player);
            } else if(task.type == "remove") {
                pool.remove(task.player);
            }
        }
    }
}

class MatchCloneFactory : virtual public MatchIfFactory {
    public:
        ~MatchCloneFactory() override = default;
        MatchIf* getHandler(const ::apache::thrift::TConnectionInfo& connInfo) override
        {
            std::shared_ptr<TSocket> sock = std::dynamic_pointer_cast<TSocket>(connInfo.transport);
            /*cout << "Incoming connection\n";
            cout << "\tSocketInfo: "  << sock->getSocketInfo() << "\n";
            cout << "\tPeerHost: "    << sock->getPeerHost() << "\n";
            cout << "\tPeerAddress: " << sock->getPeerAddress() << "\n";
            cout << "\tPeerPort: "    << sock->getPeerPort() << "\n";*/
            return new MatchHandler;
        }
        void releaseHandler(MatchIf* handler) override {
            delete handler;
        }
};

int main(int argc, char **argv) {
    TThreadedServer server(
            std::make_shared<MatchProcessorFactory>(std::make_shared<MatchCloneFactory>()),
            std::make_shared<TServerSocket>(9090), //port
            std::make_shared<TBufferedTransportFactory>(),
            std::make_shared<TBinaryProtocolFactory>());

    printf("Starting Matching Server...\n");

    thread matching_thread(consume_task);

    server.serve();
    return 0;
}
