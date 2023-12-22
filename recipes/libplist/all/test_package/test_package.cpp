#include <plist/plist.h>
#include <plist/plist++.h>
#include <iostream>

int main(int argc, const char* argv[])
{
    plist_t str = plist_new_string("Test");

    PList::String str2(str);

    std::string str3 = str2.GetValue();

    std::cout << str3 << std::endl;

    return 0;
}
