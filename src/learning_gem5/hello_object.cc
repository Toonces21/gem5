#include "debug/Hello.hh"
#include "hello_object.hh"

//Constructor for HelloObject.
//DPRINTF is a C++ macro.
HelloObject::HelloObject(HelloObjectParams *params) :
    SimObject(params), event(*this), timesLeft(10), latency(100){
  DPRINTF(Hello, "Created the hello object\n");
};

//Used by the SimObject py declr to return new SimObject.
HelloObject* HelloObjectParams::create(){
    return new HelloObject(this);
}

//Function that defines what happens during the event
void HelloObject::processEvent(){
    timesLeft--;
    DPRINTF(Hello, "Hello world! Processing the event! %d left\n", timesLeft);
    if (timesLeft <= 0)
      DPRINTF(Hello, "Done firing!\n");
    else
      schedule(event, curTick() + latency);
}

//Function that schedules the event at the given tick. Tick 100 in this case.
void HelloObject::startup(){
  schedule(event, latency);
}
