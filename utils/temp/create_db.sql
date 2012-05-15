BEGIN;
CREATE TABLE "categories" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL UNIQUE,
    "slug" varchar(50) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "is_active" boolean NOT NULL,
    "meta_keywords" varchar(255) NOT NULL,
    "meta_description" varchar(255) NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL,
    "parent_id" integer,
    "lft" integer CHECK ("lft" >= 0) NOT NULL,
    "rght" integer CHECK ("rght" >= 0) NOT NULL,
    "tree_id" integer CHECK ("tree_id" >= 0) NOT NULL,
    "level" integer CHECK ("level" >= 0) NOT NULL
)
;
ALTER TABLE "categories" ADD CONSTRAINT "parent_id_refs_id_2d747e89" FOREIGN KEY ("parent_id") REFERENCES "categories" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "products_categories" (
    "id" serial NOT NULL PRIMARY KEY,
    "product_id" integer NOT NULL,
    "category_id" integer NOT NULL REFERENCES "categories" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("product_id", "category_id")
)
;
CREATE TABLE "products" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "slug" varchar(255) NOT NULL UNIQUE,
    "brand" varchar(50) NOT NULL,
    "sku" varchar(50) NOT NULL,
    "price" numeric(9, 2) NOT NULL,
    "old_price" numeric(9, 2) NOT NULL,
    "is_active" boolean NOT NULL,
    "is_bestseller" boolean NOT NULL,
    "is_featured" boolean NOT NULL,
    "quantity" integer NOT NULL,
    "description" text NOT NULL,
    "meta_keywords" varchar(255) NOT NULL,
    "meta_description" varchar(255) NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
)
;
ALTER TABLE "products_categories" ADD CONSTRAINT "product_id_refs_id_7a5f8ca1" FOREIGN KEY ("product_id") REFERENCES "products" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "product_images" (
    "id" serial NOT NULL PRIMARY KEY,
    "image" varchar(100) NOT NULL,
    "description" varchar(255) NOT NULL,
    "product_id" integer NOT NULL REFERENCES "products" ("id") DEFERRABLE INITIALLY DEFERRED,
    "default" boolean NOT NULL
)
;
CREATE TABLE "characteristics_type" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    UNIQUE ("name")
)
;
CREATE TABLE "characteristics" (
    "id" serial NOT NULL PRIMARY KEY,
    "characteristic_type_id" integer NOT NULL REFERENCES "characteristics_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "value" varchar(255) NOT NULL,
    "product_id" integer NOT NULL REFERENCES "products" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("product_id", "characteristic_type_id")
)
;
CREATE INDEX "categories_parent_id" ON "categories" ("parent_id");
CREATE INDEX "categories_lft" ON "categories" ("lft");
CREATE INDEX "categories_rght" ON "categories" ("rght");
CREATE INDEX "categories_tree_id" ON "categories" ("tree_id");
CREATE INDEX "categories_level" ON "categories" ("level");
CREATE INDEX "product_images_product_id" ON "product_images" ("product_id");
CREATE INDEX "characteristics_characteristic_type_id" ON "characteristics" ("characteristic_type_id");
CREATE INDEX "characteristics_product_id" ON "characteristics" ("product_id");
COMMIT;
BEGIN;
CREATE TABLE "accounts_userprofile" (
    "id" serial NOT NULL PRIMARY KEY,
    "email" varchar(50) NOT NULL,
    "phone" varchar(20) NOT NULL,
    "shipping_name" varchar(50) NOT NULL,
    "shipping_address_1" varchar(50) NOT NULL,
    "shipping_address_2" varchar(50) NOT NULL,
    "shipping_city" varchar(50) NOT NULL,
    "shipping_country" varchar(50) NOT NULL,
    "shipping_zip" varchar(10) NOT NULL,
    "billing_name" varchar(50) NOT NULL,
    "billing_address" varchar(50) NOT NULL,
    "billing_city" varchar(50) NOT NULL,
    "billing_country" varchar(50) NOT NULL,
    "billing_zip" varchar(10) NOT NULL,
    "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
COMMIT;
BEGIN;
CREATE TABLE "cart_items" (
    "id" serial NOT NULL PRIMARY KEY,
    "cart_id" varchar(50) NOT NULL,
    "date_added" timestamp with time zone NOT NULL,
    "quantity" integer NOT NULL,
    "product_id" integer NOT NULL REFERENCES "products" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE INDEX "cart_items_product_id" ON "cart_items" ("product_id");
COMMIT;
BEGIN;
CREATE TABLE "checkout_order" (
    "id" serial NOT NULL PRIMARY KEY,
    "email" varchar(50) NOT NULL,
    "phone" varchar(20) NOT NULL,
    "shipping_name" varchar(50) NOT NULL,
    "shipping_address_1" varchar(50) NOT NULL,
    "shipping_address_2" varchar(50) NOT NULL,
    "shipping_city" varchar(50) NOT NULL,
    "shipping_country" varchar(50) NOT NULL,
    "shipping_zip" varchar(10) NOT NULL,
    "billing_name" varchar(50) NOT NULL,
    "billing_address" varchar(50) NOT NULL,
    "billing_city" varchar(50) NOT NULL,
    "billing_country" varchar(50) NOT NULL,
    "billing_zip" varchar(10) NOT NULL,
    "date" timestamp with time zone NOT NULL,
    "status" integer NOT NULL,
    "ip_address" inet NOT NULL,
    "last_updated" timestamp with time zone NOT NULL,
    "user_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "transaction_id" varchar(20) NOT NULL
)
;
CREATE TABLE "checkout_orderitem" (
    "id" serial NOT NULL PRIMARY KEY,
    "product_id" integer NOT NULL REFERENCES "products" ("id") DEFERRABLE INITIALLY DEFERRED,
    "quantity" integer NOT NULL,
    "price" numeric(9, 2) NOT NULL,
    "order_id" integer NOT NULL REFERENCES "checkout_order" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE INDEX "checkout_order_user_id" ON "checkout_order" ("user_id");
CREATE INDEX "checkout_orderitem_product_id" ON "checkout_orderitem" ("product_id");
CREATE INDEX "checkout_orderitem_order_id" ON "checkout_orderitem" ("order_id");
COMMIT;
BEGIN;
CREATE TABLE "news" (
    "id" serial NOT NULL PRIMARY KEY,
    "header" varchar(255) NOT NULL,
    "slug" varchar(255) NOT NULL UNIQUE,
    "body" text NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "updated" timestamp with time zone,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "views" integer NOT NULL
)
;
CREATE INDEX "news_user_id" ON "news" ("user_id");
COMMIT;
BEGIN;
CREATE TABLE "search_terms" (
    "id" serial NOT NULL PRIMARY KEY,
    "query" varchar(50) NOT NULL,
    "search_date" timestamp with time zone NOT NULL,
    "ip_address" inet NOT NULL,
    "user_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE INDEX "search_terms_user_id" ON "search_terms" ("user_id");
COMMIT;
