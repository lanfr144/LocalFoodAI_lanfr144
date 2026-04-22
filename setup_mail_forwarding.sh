#!/bin/bash
# run this as root/sudo on the Ubuntu VM

echo "Setting up centralized mail forwarding to lanfr144@gmail.com..."

# 1. Update the skeleton directory so all NEW users created automatically forward mail
echo "lanfr144@gmail.com" | sudo tee /etc/skel/.forward
sudo chmod 644 /etc/skel/.forward

# 2. Add forwarding to all dynamically created home directories
for user_dir in /home/*; do
  if [ -d "$user_dir" ]; then
    user_name=$(basename "$user_dir")
    echo "lanfr144@gmail.com" | sudo tee "$user_dir/.forward"
    sudo chown "$user_name":"$user_name" "$user_dir/.forward"
    sudo chmod 644 "$user_dir/.forward"
    echo "Configured for user: $user_name"
  fi
done

# 3. Add forwarding for root manually
echo "lanfr144@gmail.com" | sudo tee /root/.forward
sudo chmod 644 /root/.forward
echo "Configured for root."

echo "✅ All system mail will now forward to lanfr144@gmail.com"
