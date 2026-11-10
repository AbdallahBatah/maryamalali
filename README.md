# macro by maryam

Bilingual (English / Arabic) website for Emirati macro photographer **Maryam Aalali**, with an availability calendar, bank-transfer booking form and an admin panel.

## Folders

| Folder | What it is |
| --- | --- |
| `public/` | The website. Deploy this folder as-is to any static host (Netlify, Vercel, Cloudflare Pages, cPanel). English pages at the root, Arabic in `public/ar/`, admin at `public/admin.html`. |
| `supabase/` | `schema.sql` (tables, security rules, booking function, storage) and `seed.sql` (starter content). Run both once in the Supabase SQL Editor. |
| `src/` | Source used to generate the HTML pages: `build.py`, styles and scripts. Edit here, then run `python3 src/build.py` to regenerate `public/`. |
| `originals/` | Source material: original photos, full-resolution portfolio images, brand guidelines and portfolio PDF. Not deployed. |
| `SETUP.md` | Step-by-step go-live guide: Supabase, admin login, connecting the site, publishing, testing. |

## Going live

1. Follow `SETUP.md` to create the Supabase project and Maryam's admin login.
2. Put the Supabase Project URL and anon key in `public/assets/config.js`.
3. Deploy `public/`. Until `config.js` is filled, the booking page and admin run in preview mode with example data.

## Editing content

- Trips, bookings, bank details, contact details, FAQ and gallery: in the admin panel (`/admin.html`).
- Page texts, SEO titles and descriptions, alt text and menus: in `src/build.py`, then rebuild (needs Python 3 and Pillow: `pip install pillow`).
- The site domain is set in `src/build.py` (`DOMAIN`). It is used in canonical links, hreflang, `sitemap.xml`, `robots.txt` and `llms.txt`.

Brand identity by Ola Allouz. All photographs © Maryam Aalali.
