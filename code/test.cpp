#include <iostream>
#include <vector>

std::vector<int> decimalToBinary(int decimal) {
    std::vector<int> binary;
    
    while (decimal > 0) {
        binary.push_back(decimal % 2);
        decimal /= 2;
    }
    
    return binary;
}

int main() {
    int decimal = 10;
    std::vector<int> binary = decimalToBinary(decimal);
    
    std::cout << "Binary representation of " << decimal << " is: ";
    for (int i = binary.size() - 1; i >= 0; i--) {
        std::cout << binary[i];
    }
    
    return 0;
}
