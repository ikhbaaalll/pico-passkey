# pico-passkey

A DIY hardware passkey: a Waveshare **RP2350-Zero** flashed with **pico-fido**,
carried on a keychain, used for GitHub and anything else that takes a FIDO2 key.

Plan and open decisions live in `~/goals/PICO-PASSKEY-GOAL.md`.
Step-by-step setup: [`docs/PLUG-AND-GO.md`](docs/PLUG-AND-GO.md).

## Why

A passkey is a keypair per site. The private half is generated in the chip and
never leaves it; the site keeps the public half. Login is a signature over a
challenge bound to the site's domain, so a fake domain gets a signature it cannot
use. There is no secret to steal off a server.

- Discoverable (passkey) credentials: **256** on pico-fido. A YubiKey 5 holds 100.
- Non-discoverable (U2F / 2FA): **unlimited** — the credential lives in the ID the
  server holds.

## Parts

| Part | Why |
| --- | --- |
| Waveshare RP2350-Zero (RP2350A, 4 MB flash, USB-C) | Prebuilt pico-fido image. Rp149.000. |
| USB-C to USB-C **data** cable | Flash and test. A charge-only cable will not expose the key. |
| USB-C male OTG adapter | Only for a USB-A-only host. Buy after development. |
| 3D printed case | Carry. Printables `1515646` or MakerWorld `937167`, PETG. |

Do not use an RP2040 board: no OTP, no secure boot, the flash dumps and takes the
keys with it.

## Flash

1. Hold **BOOT**, plug the cable in. A drive named `RP2350` mounts.
2. Copy `pico_fido_waveshare_rp2350_zero-6.6.uf2` from the pico-fido release page
   onto it. The board reboots as a Pico Key.
3. Commission at the PicoKeys web console (Chrome or Edge, WebUSB):
   vendor **Waveshare**, model **RP2350-Zero**, LED driver **Single**,
   **Secure Boot + Secure Lock ON**. Secure Boot and Secure Lock need the RP2350;
   they seal the master key in OTP so a stolen board yields nothing.
4. Register the key on <https://webauthn.io> to confirm.
5. GitHub: Settings → Password and authentication → Passkeys → Add a passkey.

## Test

```sh
uv run --with fido2 python passkey_smoke.py            # presence + info
uv run --with fido2 python passkey_smoke.py --register # full make/assert, touch when asked
```

`--register` makes a discoverable credential for `example.com` on the device and
then asserts with it. A touch prompt appears; press the board's BOOT button.

No device found, or a wrong image, prints one line and exits non-zero.

## Caveats

- **Not FIDO Certified.** GitHub accepts self-attestation. Some enterprise and bank
  sites reject it. Test each site before you depend on the key there.
- **No NFC.** Phone login needs the wired adapter.
- **Lost key with no backup locks every account on it.** Register a second factor
  on every account you care about before the key carries it alone.
- pico-fido runs one firmware at a time. FIDO and OpenPGP do not coexist; switching
  needs the data-wipe image first.
