# Plug and go — RP2350-Zero passkey

One page. Follow top to bottom. Roughly 15 minutes.

## What you need

- The board (Waveshare RP2350-Zero).
- A USB-C to USB-C **data** cable. A charge-only cable powers the board but the
  computer never sees it. If unsure, test the cable on a phone or an SSD first —
  if nothing mounts, it is charge-only.
- Chrome or Edge on a laptop. The commission step uses WebUSB, which Firefox and
  Safari do not support.

## 1. Flash pico-fido

1. Unplug the board.
2. Hold the **BOOT** button. Keep holding.
3. Plug the cable in. Release BOOT.
4. A drive named `RP2350` appears in your file manager.
5. Download the RP2350-Zero image from the pico-fido releases:
   <https://github.com/polhenarejos/pico-fido/releases>
   File name looks like `pico_fido_waveshare_rp2350_zero-<version>.uf2`.
6. Drag the `.uf2` file onto the `RP2350` drive.
7. The drive unmounts on its own. The board reboots as a key. The RGB LED blinks.

If the drive never appears: try another cable, then another USB port. Hold BOOT
before the plug, not after.

## 2. Commission (once)

1. Open <https://picokeys.com> in Chrome or Edge, go to the commissioning page.
2. Hold BOOT, plug in, release. The web page should find the board.
3. Set:
   - Vendor: **Waveshare**
   - Model: **RP2350-Zero**
   - LED driver: **Single**
   - Product name: anything, e.g. `PicoHack`
   - Secure Boot: **ON**
   - Secure Lock: **ON**
4. Press **Commission**. Wait for the LED confirmation.
5. Unplug, plug back in.

Secure Boot and Secure Lock seal the keys in chip hardware. A thief who steals the
board gets nothing. They are hard to undo, so set them now, while the board holds
no real accounts.

## 3. Confirm it works

1. Open <https://webauthn.io> in Chrome or Edge.
2. Type any username, press **Register**.
3. A browser prompt appears. Pick **security key** — not Windows Hello, not the
   phone. Press the board's **BOOT** button when asked.
4. It registers. Press **Authenticate**, tap the button again, and it logs in.

Or run the repo check with the board plugged in:

```sh
uv run --with fido2 python passkey_smoke.py --register
```

## 4. Add it to GitHub

1. GitHub → your avatar → **Settings** → **Password and authentication**.
2. Under **Passkeys**, click **Add a passkey**.
3. Enter your password if asked.
4. At the browser prompt, choose **security key** / **use a different device**.
   Press the board's button.
5. Name it `Pico board`, click **Done**.

Your account now holds the Windows passkey and the board passkey. Both work. The
board entry shows no `Synced` label — that is correct, it is device-bound.

## 5. Carry it (later)

- USB-C male OTG adapter (or a C-to-A cable) for USB-A-only ports.
- A 3D printed case. Print in PETG, 25–30% infill.

## If something goes wrong

| Symptom | Cause | Fix |
| --- | --- | --- |
| No drive appears | Cable is charge-only, or BOOT not held at plug-in | Another cable; hold BOOT before the plug |
| `RP2350` drive appears but flashing does nothing | Wrong image | Confirm the file name says `waveshare_rp2350_zero` |
| Browser prompt shows only Windows Hello | The browser picked the platform authenticator | Choose "use a different device" / "security key" |
| The device exists but GitHub rejects it | Rare site policy | Register a different factor for that site |
| Board dead after Secure Lock | Locked firmware mismatch | Recovery image from the PicoKeys site |

## Rules that save you

- Never enable Secure Boot before you have a working flash. Confirm step 3 first.
- Attestation may fail on banks and enterprise sites. Test each site before you
  drop the password from it.
- Windows Hello and GitHub Mobile already hold your GitHub account, so a lost
  board locks nothing today. Keep it that way — never leave an account with the
  board as its only factor.
