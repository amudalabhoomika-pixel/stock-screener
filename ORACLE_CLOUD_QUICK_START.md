# 🚀 Oracle Cloud Quick Start (2 minutes)

## Step 1: Create Free Account
1. Go: https://www.oracle.com/cloud/free/
2. Click "Start for Free"
3. Verify email + phone
4. **Done!** No credit card needed

## Step 2: Create VM
1. Click "Create a VM instance"
2. Name: `stock-screener`
3. Image: Ubuntu 22.04
4. Shape: Ampere (Always Free)
5. **Download SSH Key** → Save as `id_rsa.key`
6. Click Create

## Step 3: Open Port 5000
1. Go to Networking → VCN
2. Edit Ingress Rules
3. Add rule:
   ```
   Source: 0.0.0.0/0
   Protocol: TCP
   Port: 5000
   ```

## Step 4: Deploy (One Command!)
```bash
# SSH to VM
ssh -i id_rsa.key ubuntu@YOUR_VM_IP

# Run one command
git clone https://github.com/amudalabhoomika-pixel/stock-screener.git && \
cd stock-screener && \
chmod +x deploy.sh && \
bash deploy.sh
```

When prompted, enter your Telegram credentials.

## Step 5: Access Dashboard
```
http://YOUR_VM_IP:5000
```

## ✅ Done!
Your app is now running 24/7, completely free!

### Commands
```bash
# View logs
tail -f logs/app.log

# Restart app
bash restart.sh

# Stop app
bash stop.sh
```

### Find Your VM IP
In Oracle Cloud Console:
1. Go to Compute → Instances
2. Click your instance
3. Copy "Public IP Address"

---

**🎉 That's it! Stock alerts will run every weekday at 9:30 AM ET automatically!**
