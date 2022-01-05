# Create an indirect rule base
def addup_indirect_ruleslibrary(list, key1, key2, value1, value2):
    while (1):
        str1 = input("Please enter animal properties (space separated, end with 0): ")
        if (str1 == '0'): break
        a = str1.split()
        key1.append(a)

        str2 = input("Please enter the result：")
        value1.append(str2)

        # Add the individual attributes of the animal to the rule base antecedent
        len1 = len(a)
        for i in range(0, len1):
            if i not in list:
                list.append(a[i])

    return 1

# Create a direct rule base
def addup_direct_ruleslibrary(list, key1, key2, value1, value2):
    while (1):
        str1 = input("Please enter animal properties (space separated, end with 0): ")
        if (str1 == '0'): break
        a = str1.split()
        key2.append(a)

        str2 = input("Please enter the result：")
        value2.append(str2)

        # Add the individual attributes of the animal to the rule base antecedent
        len2 = len(a)
        for i in range(0, len2):
            if i not in list:
                list.append(a[i])

    return 1

# Create the rule base
def init(list, key1, key2, value1, value2):
    print("\nCreate an indirect rule base！\n")
    addup_indirect_ruleslibrary(list, key1, key2, value1, value2)
    print("\nThe indirect rule base is built！\n")

    print("Create a direct rule base！\n")
    addup_direct_ruleslibrary(list, key1, key2, value1, value2)
    print("\nThe rule base is established！\n")

    return 1

# Animal identification
def recognize(list, key1, key2, value1, value2):
    map = { } # Comprehensive database. 1 indicates that the information has been added to the comprehensive database
    len1 = len(list)
    for i in range(0, len1): map[list[i]] = 0 # Initializes the comprehensive database

    str = input("Please enter animal properties :(space separated)")
    list1 = str.split()
    len1 = len(list1)
    for i in range(0, len1): map[list1[i]] = 1 # Add to the comprehensive database

    # Identified in the indirect rule base
    len1 = len(key1)
    for i in range(0, len1):
        list2 = key1[i]
        len2 = len(list2)
        flag = 1
        for j in range(0, len2):
            if(map[list2[j]] == 0): # An element of the antecedent item of the rule library does not exist in the comprehensive database, that is, the two do not match
                flag = 0
                break

        if(flag):
            map[value1[i]] = 1

    # Identified in the direct rule base
    len1 = len(key2)
    for i in range(0, len1):
        list2 = key2[i]
        len2 = len(list2)
        flag = 1
        for j in range(0, len2):
            if (map[list2[j]] == 0): # An element of the antecedent item of the rule library does not exist in the comprehensive database, that is, the two do not match
                flag = 0
                break

        if (flag):
            return value2[i]

    return "Failed identification ! "

def solve(list, key1, key2, value1, value2):
    while(1):
        print("\n1. Add the direct rule library."
              "2. Add the indirect rule library."
              "3. Do animal identification."
              "4. Exit the program!\n")
        n = int(input("Please select ："))
        if (n == 1):
            addup_direct_ruleslibrary(list, key1, key2, value1, value2)
        elif(n == 2):
            addup_indirect_ruleslibrary(list, key1, key2, value1, value2)
        elif(n == 3):
            str = recognize(list, key1, key2, value1, value2)
            print("The animal is：",str)
        elif(n == 4):
            print("\nSuccessful exit procedure！\n")
            break
        else:
            print("\nPlease re-enter！\n")

    return 1

def main():
    list = [ ]  # Store rule base antecedents 
    key1 = [ ]  # Store indirected rule base antecedents 
    key2 = [ ]  # Store directed rule base antecedents 
    value1 = [ ] # Store indirected rule base antecedents 
    value2 = [ ] # Store directed rule base antecedents  
    init(list, key1, key2, value1, value2) # Initializes the rule base
    solve(list, key1, key2, value1, value2)

main()
