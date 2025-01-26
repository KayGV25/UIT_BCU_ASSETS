# Setting and Checking NAT Router for SSH Server in iptables

## 1. Enable IP Forwarding

Ensure that the system is configured to forward packets. Run the following command:

```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
sudo sysctl -w net.ipv4.ip_forward=1
```

Make it persistent by adding the following line to `/etc/sysctl.conf`:

```bash
net.ipv4.ip_forward=1
```

Then apply the changes:

```bash
sysctl -p
```

---

## 2. Set Up NAT Rules in `iptables`

Suppose:

- The public IP address of the router is `203.0.113.1`.
- The private IP address of the SSH server is `192.168.1.100`.
- SSH server listens on port `22`.

### a. Add a PREROUTING Rule to Redirect Traffic

Run this command to forward incoming SSH traffic from the public IP (`203.0.113.1`) to the private SSH server (`172.19.90.72`):

```bash
iptables -t nat -A PREROUTING -p tcp --dport 22 -j DNAT --to-destination 172.19.90.72:22
iptables -t nat -A PREROUTING -p udp --dport 22 -j DNAT --to-destination 172.19.90.72:22
```

### b. Add a POSTROUTING Rule for Outgoing Traffic

Run this command to ensure the outgoing traffic is routed back properly:

```bash
iptables -t nat -A POSTROUTING -p tcp -d 172.19.90.72 --dport 22 -j MASQUERADE
iptables -t nat -A POSTROUTING -p udp -d 172.19.90.72 --dport 22 -j MASQUERADE
```

---

## 3. Check NAT Rules

To verify that the rules have been added, use the following commands:

### View PREROUTING Rules

```bash
iptables -t nat -L PREROUTING -v -n
```

### View POSTROUTING Rules

```bash
iptables -t nat -L POSTROUTING -v -n
```

---

## 4. Save the Rules

Make sure the `iptables` rules persist across reboots. Save the rules with:

- For `iptables-persistent` package:

    ```bash
    sudo bash -c "iptables-save > /etc/iptables/rules.v4"
    ```

- For `iptables.service`:

    ```bash
    service iptables save
    ```

---

## 5. Test the SSH Connection

From an external machine, connect to the SSH server using the router's public IP:

```bash
ssh user@203.0.113.1
```

If the setup is correct, the connection will be forwarded to the internal SSH server at `192.168.1.100`.

---

## Troubleshooting

- Ensure no firewall or security group is blocking port `22` on the router or the SSH server.
- Verify the SSH server is running and listening on `192.168.1.100:22` using:

    ```bash
    netstat -tuln | grep :22
    ```

- Check the `iptables` logs for dropped packets if connectivity fails. Add a logging rule to troubleshoot:

    ```bash
    iptables -A INPUT -j LOG --log-prefix "iptables INPUT: " --log-level 4
    
