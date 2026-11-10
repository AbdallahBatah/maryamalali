# macro by maryam: go-live guide

The website works in **preview mode** until it is connected to Supabase (database, file storage and admin login). In preview mode the calendar shows example dates and nothing is saved for real. Follow these steps once.

## 1. Create the Supabase project (10 minutes)

1. Sign up at supabase.com and create a new project. Choose the region closest to the UAE that is offered, and save the database password somewhere safe.
2. Open **SQL Editor → New query**, paste the whole of `supabase/schema.sql`, and click **Run**.
3. New query again: paste `supabase/seed.sql` and **Run**. This loads the bank details, contact details, the 12 FAQ answers, the 20 gallery photos, and a hidden "Macro Walk" template trip.

## 2. Create Maryam's admin login

1. **Authentication → Users → Add user → Create new user**. Enter Maryam's email and a strong password, and tick **Auto confirm user**.
2. **Authentication → Sign In / Providers**: turn **off** "Allow new users to sign up". Only accounts you create can sign in.
3. SQL Editor, run (with her real email):

```sql
insert into public.admins (user_id)
select id from auth.users where email = 'maryamaalali@live.com';
```

To add a second admin later, create the user the same way and run the same query with their email.

## 3. Connect the website

1. **Project Settings → API**. Copy the **Project URL** and the **anon public** key.
2. Open `assets/config.js` and paste them:

```js
window.MBM_CONFIG = {
  supabaseUrl: "https://xxxx.supabase.co",
  supabaseAnonKey: "eyJ..."
};
```

The anon key is designed to be public. Never paste the `service_role` key into the website.

## 4. Publish the site

Upload the whole folder (keep the structure: `index.html`, `ar/`, `assets/`, `img/`, `sitemap.xml`, `robots.txt`, `llms.txt`) to any static host: Netlify (drag and drop), Vercel, Cloudflare Pages, or cPanel `public_html`. The `supabase/` folder and this guide don't need to be uploaded.

**Domain:** the site assumes `https://macrobymaryam.com`. If the domain is different, find and replace `https://macrobymaryam.com` in all `.html` files, `sitemap.xml`, `robots.txt` and `llms.txt` before uploading.

After launch, submit `https://YOUR-DOMAIN/sitemap.xml` in Google Search Console.

## 5. Test once

1. Go to `/admin.html` and sign in.
2. **Calendar & trips**: open the hidden Macro Walk template, use **Duplicate to this date** with a future date, then open the copy, tick **Visible on the website**, and save.
3. On `/book.html`, book that trip with a test receipt image.
4. In the admin **Bookings**, open it, check the receipt shows, then **Cancel booking** (the seats return to the calendar).

## Daily use (for Maryam)

- **Calendar & trips**: click **+** on a day to add a trip; click a trip to edit price, seats, time, place, what's included, rules, or hide it.
- **Bookings**: new ones arrive as **Pending**. Open the booking, check the transfer receipt against the bank, then **Confirm payment**. Use the WhatsApp link to message the family. **Export CSV** gives a roster for the day.
- **Payment details / Contact details / FAQ / Gallery**: edit and save; the website shows the change immediately.

## Good to know

- **Seats** are checked by the database at the moment of booking, so two people can't take the last seat at the same time. Cancelled bookings free their seats.
- **Privacy**: bookings include children's names and ages and allergy details. Only admins can read bookings and receipts. Delete bookings and receipts you no longer need (for example, after each season).
- **Email alerts** for new bookings are not set up yet. A simple next step is a Supabase Database Webhook on the `bookings` table that sends an email through a service such as Resend.
- **Supabase free plan**: projects on the free plan may pause after a period without activity. Check Supabase's current plan terms; the paid plan keeps the project always on.
- Text and photos edited in the admin appear for visitors straight away. Search engines pick them up as they re-crawl the pages.
