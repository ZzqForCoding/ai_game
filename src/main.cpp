// This autogenerated skeleton file illustrates how to build a server.
// You should copy it to another filename to avoid overwriting it.

#include "code_running_server/CodeRunning.h"
#include <thrift/concurrency/ThreadManager.h>
#include <thrift/concurrency/ThreadFactory.h>
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/server/TThreadPoolServer.h>
#include <thrift/server/TThreadedServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TSocket.h>
#include <thrift/transport/TTransportUtils.h>
#include <thrift/TToString.h>
#include <thrift/transport/TBufferTransports.h>

#include <boost/filesystem.hpp>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <sstream>
#include <fstream>
#include <exception>
#include "thread"
#include "mutex"
#include "condition_variable"
#include "queue"

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;

using namespace  ::code_running_service;

using namespace std;
typedef pair<int, int> PII;

struct MessageQueue {
    queue<Bot> q;
    mutex m;
    condition_variable cv;
} message_queue;

struct Result
{
    int status;
    string output;
    string error;
};

class CodeRunningHandler : virtual public CodeRunningIf {
    public:
        CodeRunningHandler() {
            // Your initialization goes here
        }

        int32_t add_bot_code(const Bot& bot, const std::string& info) {
            // Your implementation goes here
            unique_lock<mutex> lock1(message_queue.m);
            message_queue.q.push(bot);
            message_queue.cv.notify_all();
            return 0;
        }

};

class CodeRunningCloneFactory : virtual public CodeRunningIfFactory {
    public:
        ~CodeRunningCloneFactory() override = default;
        CodeRunningIf* getHandler(const ::apache::thrift::TConnectionInfo& connInfo) override
        {
            std::shared_ptr<TSocket> sock = std::dynamic_pointer_cast<TSocket>(connInfo.transport);
            /*cout << "Incoming connection\n";
              cout << "\tSocketInfo: "  << sock->getSocketInfo() << "\n";
              cout << "\tPeerHost: "    << sock->getPeerHost() << "\n";
              cout << "\tPeerAddress: " << sock->getPeerAddress() << "\n";
              cout << "\tPeerPort: "    << sock->getPeerPort() << "\n";*/
            return new CodeRunningHandler;
        }
        void releaseHandler(CodeRunningIf* handler) override {
            delete handler;
        }
};

vector<string> split(const string& str, const string& sep) {
    vector<string> ret;
    if("" == str) return ret;

    //先将要切割的字符串从string类型转换为char*类型
    char *strs = new char[str.length() + 1] ;
    strcpy(strs, str.c_str());

    char *seps = new char[sep.length() + 1];
    strcpy(seps, sep.c_str());

    char *p = strtok(strs, seps);
    while(p) {
        string s = p;     //分割得到的字符串转换为string类型
        ret.push_back(s); //存入结果数组
        p = strtok(NULL, seps);
    }

    return ret;
}

string concatStr(string one, string two, string three="", string four="", string five="") {
    return one + two + three + four + five;
}

bool check_tail_increasing(int step) {
    if(step <= 10) return true;
    return step % 3 == 1;
}

vector<PII> getCells(int sx, int sy, string steps) {
    steps = steps.substr(1, steps.length() - 2);
    vector<PII> ret;

    int dx[] = {-1, 0, 1, 0}, dy[] = {0, 1, 0, -1};
    int x = sx, y = sy;
    int step = 0;
    ret.push_back({x, y});
    for(int i = 0; i < steps.length(); i++) {
        int d = steps[i] - '0';
        x += dx[d], y += dy[d];
        ret.push_back({x, y});
        if(!check_tail_increasing(++step)) {
            ret.erase(ret.begin());
        }
    }
    return ret;
}

std::string generate_tmpfile_name()
{
    std::ostringstream ss;
    ss << "/tmp/" << boost::filesystem::unique_path().native();
    return ss.str();
}

Result exec(std::string command)
{
    const auto out_file = generate_tmpfile_name();
    const auto err_file = generate_tmpfile_name();

    // Redirect output of the command appropriately
    std::ostringstream ss;
    ss << command.c_str() << " >" << out_file << " 2>" << err_file;
    const auto cmd = ss.str();

    // Call the command
    const auto status = std::system(cmd.c_str());

    // Read the output from the files and remove them
    std::ostringstream out_stream;
    std::ostringstream err_stream;
    ifstream infile1(out_file);
    out_stream << infile1.rdbuf();
    infile1.close();
    ifstream infile2(err_file);
    err_stream << infile2.rdbuf();
    infile2.close();
    std::remove(out_file.c_str());
    std::remove(err_file.c_str());

    // Store the output
    Result result;
    result.status = status;
    result.output = out_stream.str();
    result.error  = err_stream.str();

    return result;
}

void run(Bot bot) {
    string dockerId;
    Result result = exec("docker run -itd code_runner:2.0 /bin/bash");
    dockerId = result.output.substr(0, 12);
    // 分配的不准
    system(concatStr("docker update ", dockerId, " --memory 64MB --memory-swap -1").c_str());
    cout << bot.userId << endl;

    bot.botCode.replace(bot.botCode.find("main"), 4, "main123456789");

    bot.botCode += "\n\n#include <thread>\n\
#include <unistd.h>\n\n\
void startTime() {\n\
    int x = 0;\n\
    while(true) {\n\
        sleep(1);\n\
        if(++x >= 1) {\n\
            cerr << \"Time Limit Exceeded\";\n\
            exit(0);\n\
        }\n\
    }\n\
}\n\n\
int main() {\n\
    freopen(\"/tmp/input.txt\", \"r\", stdin);\
    thread t(startTime);\n\
    t.detach();\n\
    main123456789();\n\
    return 0;\n\
}\n";

    system(concatStr("echo '", bot.botCode, "' > /tmp/code.cpp").c_str());
    system(concatStr("docker cp /tmp/code.cpp ", dockerId, ":/tmp/code.cpp").c_str());
    // 地图#my.sx#my.sy#my操作#you.sx#you.sy#you操作
    vector<string> v = split(bot.input, "#");
    string newInput;
    for(int i = 0, k = 0; i < 13; i++) {
        for(int j = 0; j < 14; j++, k++) {
            if(v[0][k] == '0') newInput += "0 ";
            else newInput += "1 ";
        }
        newInput += "\n";
    }
    newInput += "\n";

    vector<PII> aCells = getCells(stoi(v[1]), stoi(v[2]), v[3]);
    vector<PII> bCells = getCells(stoi(v[4]), stoi(v[5]), v[6]);

    for(int i = 0; i < aCells.size(); i++)
        newInput += to_string(aCells[i].first) + " " + to_string(aCells[i].second) + "\n";

    newInput += "\n";

    for(int i = 0; i < aCells.size(); i++)
        newInput += to_string(bCells[i].first) + " " + to_string(bCells[i].second) + "\n";

    system(concatStr("echo '", newInput, "' > /tmp/intput.txt").c_str());
    system(concatStr("docker cp /tmp/input.txt ", dockerId, ":/tmp/input.txt").c_str());
    Result compile, codeResult;
    try {
        compile = exec(concatStr("docker exec ", dockerId, " g++ -Wall -o /tmp/code.out /tmp/code.cpp -pthread").c_str());
        codeResult = exec(concatStr("test -e /tmp/code.out && docker exec ", dockerId, " /tmp/code.out"));
    } catch(exception e) {
        cout << "except" << endl;
    }
    compile.error.replace(compile.error.find("main123456789"), 13, "main");
    cout << "compile code: " << compile.status << " , output: " << compile.output << " ,error: " << compile.error << endl;
    if(result.status == 35584) codeResult.error = "Memory Limit Exceeded";

    cout << "result status: " << codeResult.status << " , output: " << codeResult.output << " , error: " << codeResult.error << endl;

    system(concatStr("docker stop ", dockerId).c_str());
    system(concatStr("docker rm ", dockerId).c_str());
}

void consume_task() {
    while(true) {
        unique_lock<mutex> lock1(message_queue.m);
        if(message_queue.q.empty()) {
            message_queue.cv.wait(lock1);
        } else {
            Bot bot = message_queue.q.front();
            message_queue.q.pop();
            lock1.unlock();
            run(bot);
        }
    }
}

int main(int argc, char **argv) {
    TThreadedServer server(
            std::make_shared<CodeRunningProcessorFactory>(std::make_shared<CodeRunningCloneFactory>()),
            std::make_shared<TServerSocket>(9090), //port
            std::make_shared<TBufferedTransportFactory>(),
            std::make_shared<TBinaryProtocolFactory>());

    printf("Starting BotRunning Server...\n");

    thread code_running_thread(consume_task);

    server.serve();
    return 0;
}

