#pragma once

module Demo
{

interface Hello
{
    idempotent void setLocation(float x, float y, float z);
    void shutdown();
};

};
