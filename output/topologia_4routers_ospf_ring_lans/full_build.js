addDevice("R-LAN1", "2911", 220, 100);
addDevice("R-LAN2", "2911", 620, 100);
addDevice("R-LAN3", "2911", 620, 420);
addDevice("R-LAN4", "2911", 220, 420);
addDevice("SW-LAN1", "2960-24TT", 220, 220);
addDevice("PC-LAN1-1", "PC-PT", 20, 340);
addDevice("PC-LAN1-2", "PC-PT", 100, 340);
addDevice("PC-LAN1-3", "PC-PT", 180, 340);
addDevice("PC-LAN1-4", "PC-PT", 260, 340);
addDevice("PC-LAN1-5", "PC-PT", 340, 340);
addDevice("LT-LAN1-1", "Laptop-PT", 180, 410);
addDevice("SW-LAN2", "2960-24TT", 620, 220);
addDevice("PC-LAN2-1", "PC-PT", 420, 340);
addDevice("PC-LAN2-2", "PC-PT", 500, 340);
addDevice("PC-LAN2-3", "PC-PT", 580, 340);
addDevice("PC-LAN2-4", "PC-PT", 660, 340);
addDevice("PC-LAN2-5", "PC-PT", 740, 340);
addDevice("LT-LAN2-1", "Laptop-PT", 580, 410);
addDevice("SW-LAN3", "2960-24TT", 620, 540);
addDevice("PC-LAN3-1", "PC-PT", 420, 660);
addDevice("PC-LAN3-2", "PC-PT", 500, 660);
addDevice("PC-LAN3-3", "PC-PT", 580, 660);
addDevice("PC-LAN3-4", "PC-PT", 660, 660);
addDevice("PC-LAN3-5", "PC-PT", 740, 660);
addDevice("LT-LAN3-1", "Laptop-PT", 580, 730);
addDevice("SW-LAN4", "2960-24TT", 220, 540);
addDevice("PC-LAN4-1", "PC-PT", 20, 660);
addDevice("PC-LAN4-2", "PC-PT", 100, 660);
addDevice("PC-LAN4-3", "PC-PT", 180, 660);
addDevice("PC-LAN4-4", "PC-PT", 260, 660);
addDevice("PC-LAN4-5", "PC-PT", 340, 660);
addDevice("LT-LAN4-1", "Laptop-PT", 180, 730);
addLink("R-LAN1", "GigabitEthernet0/0", "R-LAN2", "GigabitEthernet0/0", "cross");
addLink("R-LAN2", "GigabitEthernet0/1", "R-LAN3", "GigabitEthernet0/0", "cross");
addLink("R-LAN3", "GigabitEthernet0/1", "R-LAN4", "GigabitEthernet0/0", "cross");
addLink("R-LAN4", "GigabitEthernet0/1", "R-LAN1", "GigabitEthernet0/1", "cross");
addLink("R-LAN1", "GigabitEthernet0/2", "SW-LAN1", "GigabitEthernet0/1", "straight");
addLink("R-LAN2", "GigabitEthernet0/2", "SW-LAN2", "GigabitEthernet0/1", "straight");
addLink("R-LAN3", "GigabitEthernet0/2", "SW-LAN3", "GigabitEthernet0/1", "straight");
addLink("R-LAN4", "GigabitEthernet0/2", "SW-LAN4", "GigabitEthernet0/1", "straight");
addLink("SW-LAN1", "FastEthernet0/1", "PC-LAN1-1", "FastEthernet0", "straight");
addLink("SW-LAN1", "FastEthernet0/2", "PC-LAN1-2", "FastEthernet0", "straight");
addLink("SW-LAN1", "FastEthernet0/3", "PC-LAN1-3", "FastEthernet0", "straight");
addLink("SW-LAN1", "FastEthernet0/4", "PC-LAN1-4", "FastEthernet0", "straight");
addLink("SW-LAN1", "FastEthernet0/5", "PC-LAN1-5", "FastEthernet0", "straight");
addLink("SW-LAN1", "FastEthernet0/6", "LT-LAN1-1", "FastEthernet0", "straight");
addLink("SW-LAN2", "FastEthernet0/1", "PC-LAN2-1", "FastEthernet0", "straight");
addLink("SW-LAN2", "FastEthernet0/2", "PC-LAN2-2", "FastEthernet0", "straight");
addLink("SW-LAN2", "FastEthernet0/3", "PC-LAN2-3", "FastEthernet0", "straight");
addLink("SW-LAN2", "FastEthernet0/4", "PC-LAN2-4", "FastEthernet0", "straight");
addLink("SW-LAN2", "FastEthernet0/5", "PC-LAN2-5", "FastEthernet0", "straight");
addLink("SW-LAN2", "FastEthernet0/6", "LT-LAN2-1", "FastEthernet0", "straight");
addLink("SW-LAN3", "FastEthernet0/1", "PC-LAN3-1", "FastEthernet0", "straight");
addLink("SW-LAN3", "FastEthernet0/2", "PC-LAN3-2", "FastEthernet0", "straight");
addLink("SW-LAN3", "FastEthernet0/3", "PC-LAN3-3", "FastEthernet0", "straight");
addLink("SW-LAN3", "FastEthernet0/4", "PC-LAN3-4", "FastEthernet0", "straight");
addLink("SW-LAN3", "FastEthernet0/5", "PC-LAN3-5", "FastEthernet0", "straight");
addLink("SW-LAN3", "FastEthernet0/6", "LT-LAN3-1", "FastEthernet0", "straight");
addLink("SW-LAN4", "FastEthernet0/1", "PC-LAN4-1", "FastEthernet0", "straight");
addLink("SW-LAN4", "FastEthernet0/2", "PC-LAN4-2", "FastEthernet0", "straight");
addLink("SW-LAN4", "FastEthernet0/3", "PC-LAN4-3", "FastEthernet0", "straight");
addLink("SW-LAN4", "FastEthernet0/4", "PC-LAN4-4", "FastEthernet0", "straight");
addLink("SW-LAN4", "FastEthernet0/5", "PC-LAN4-5", "FastEthernet0", "straight");
addLink("SW-LAN4", "FastEthernet0/6", "LT-LAN4-1", "FastEthernet0", "straight");
/* === Configuraciones CLI por dispositivo ===
Copiar y pegar en la CLI de cada dispositivo. */
/* --- R-LAN1 ---
enable
configure terminal
hostname R-LAN1
no ip domain-lookup

interface GigabitEthernet0/0
 ip address 10.0.0.1 255.255.255.252
 no shutdown
 exit

interface GigabitEthernet0/1
 ip address 10.0.0.14 255.255.255.252
 no shutdown
 exit

interface GigabitEthernet0/2
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit

router ospf 1
 router-id 1.1.1.1
 network 10.0.0.0 0.0.0.3 area 0
 network 10.0.0.12 0.0.0.3 area 0
 network 192.168.1.0 0.0.0.255 area 0
 exit

end
write memory
*/ 
/* --- R-LAN2 ---
enable
configure terminal
hostname R-LAN2
no ip domain-lookup

interface GigabitEthernet0/0
 ip address 10.0.0.2 255.255.255.252
 no shutdown
 exit

interface GigabitEthernet0/1
 ip address 10.0.0.5 255.255.255.252
 no shutdown
 exit

interface GigabitEthernet0/2
 ip address 192.168.2.1 255.255.255.0
 no shutdown
 exit

router ospf 1
 router-id 2.2.2.2
 network 10.0.0.0 0.0.0.3 area 0
 network 10.0.0.4 0.0.0.3 area 0
 network 192.168.2.0 0.0.0.255 area 0
 exit

end
write memory
*/ 
/* --- R-LAN3 ---
enable
configure terminal
hostname R-LAN3
no ip domain-lookup

interface GigabitEthernet0/0
 ip address 10.0.0.6 255.255.255.252
 no shutdown
 exit

interface GigabitEthernet0/1
 ip address 10.0.0.9 255.255.255.252
 no shutdown
 exit

interface GigabitEthernet0/2
 ip address 192.168.3.1 255.255.255.0
 no shutdown
 exit

router ospf 1
 router-id 3.3.3.3
 network 10.0.0.4 0.0.0.3 area 0
 network 10.0.0.8 0.0.0.3 area 0
 network 192.168.3.0 0.0.0.255 area 0
 exit

end
write memory
*/ 
/* --- R-LAN4 ---
enable
configure terminal
hostname R-LAN4
no ip domain-lookup

interface GigabitEthernet0/0
 ip address 10.0.0.10 255.255.255.252
 no shutdown
 exit

interface GigabitEthernet0/1
 ip address 10.0.0.13 255.255.255.252
 no shutdown
 exit

interface GigabitEthernet0/2
 ip address 192.168.4.1 255.255.255.0
 no shutdown
 exit

router ospf 1
 router-id 4.4.4.4
 network 10.0.0.8 0.0.0.3 area 0
 network 10.0.0.12 0.0.0.3 area 0
 network 192.168.4.0 0.0.0.255 area 0
 exit

end
write memory
*/ 
/* --- SW-LAN1 ---
enable
configure terminal
hostname SW-LAN1
end
write memory
*/ 
/* --- SW-LAN2 ---
enable
configure terminal
hostname SW-LAN2
end
write memory
*/ 
/* --- SW-LAN3 ---
enable
configure terminal
hostname SW-LAN3
end
write memory
*/ 
/* --- SW-LAN4 ---
enable
configure terminal
hostname SW-LAN4
end
write memory
*/ 