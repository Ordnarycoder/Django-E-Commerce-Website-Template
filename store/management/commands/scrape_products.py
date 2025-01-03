from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from django.core.management.base import BaseCommand
from store.models import Product, Category, ProductImage
import time


class Command(BaseCommand):
    help = 'Scrapes products from website and stores them in the database'
    def handle(self, *args, **kwargs):
        # Reset the Product database
        print("Deleting all existing products from the database...")
        Product.objects.all().delete()


        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Set up Chrome driver
        driver = webdriver.Chrome(options=chrome_options)

        url = "https://www.websitetoscrape.com"
        driver.get(url)
        time.sleep(5)

        try:
            products = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, "//li[contains(@class, 'productListContent')]/div"))
            )
        except TimeoutException:
            print("Timeout waiting for product elements to load.")
            driver.quit()
            return

        product_links = []

        # Limit scraping to the first 5 products
        for product in products[:1]:
            try:
                product_link = product.find_element(By.XPATH, './a').get_attribute('href')
                product_links.append(product_link)
            except NoSuchElementException:
                product_links.append('')
        print(len(product_links))
        for link in product_links:
            driver.get(link)

            try:
                title = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@data-test-id='title']"))
                ).text
            except TimeoutException:
                title = None
            print(title)
            try:
                brand = driver.find_element(By.XPATH, "//h1[@data-test-id='title']/a").text
            except NoSuchElementException:
                brand = None

            images = []
            try:
                # Locate all slide items in the carousel using the constant class name
                slide_items = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ULyio3SH7sb4SNSCVAZb.pdp-slideItem"))
                )

                # Collect images from all the slides
                for slide in slide_items:
                    try:
                        image_element = slide.find_element(By.CSS_SELECTOR, "div.vLUz9wKsQbocFiC3Zlvb img")
                        img_src = image_element.get_attribute('src')
                        if img_src and img_src not in images:
                            images.append(img_src)
                    except NoSuchElementException:
                        continue

                # Locate the "Next" button (assuming this selector works as expected)
                try:
                    next_button = driver.find_element(By.XPATH, "//div[@class='sye67NQqnbH2ogwCP_2O']")
                except NoSuchElementException:
                    next_button = None

                max_iterations = 3
                iteration_count = 0

                # Loop to navigate through the carousel and collect all images
                while next_button and iteration_count < max_iterations:
                    try:
                        next_button.click()
                        time.sleep(2)
                        WebDriverWait(driver, 2)  # Wait for the DOM to update

                        # After clicking "Next," locate all slide items again
                        slide_items = driver.find_elements(By.CSS_SELECTOR, "li.ULyio3SH7sb4SNSCVAZb.pdp-slideItem")

                        # Collect images from the slides that haven't been seen yet
                        for slide in slide_items:
                            try:
                                image_element = slide.find_element(By.CSS_SELECTOR, "div.vLUz9wKsQbocFiC3Zlvb img")
                                img_src = image_element.get_attribute('src')
                                if img_src and img_src not in images:
                                    images.append(img_src)
                            except NoSuchElementException:
                                continue

                        iteration_count += 1

                    except (NoSuchElementException, TimeoutException):
                        break

                print(f"Scraped images for {title}: {images}")
            except TimeoutException:
                print(f"Failed to load carousel images for {title}.")

            try:
                rate = driver.find_element(By.XPATH, "//div[@data-test-id='has-review']/div/span").text
            except NoSuchElementException:
                rate = None

            try:
                consideration_num = driver.find_element(By.XPATH, "//div[@data-test-id='has-review']/a/b").text
            except NoSuchElementException:
                consideration_num = None

            try:
                seller = driver.find_element(By.XPATH, "//div[@data-test-id='buyBox-seller']/div/a/span").text
            except NoSuchElementException:
                seller = None

            try:
                price_string = driver.find_element(By.XPATH, "//div[@data-test-id='price-current-price']/span").text
                price = float(price_string.replace('.', '').replace(',', '.'))
            except (NoSuchElementException, ValueError):
                price = 0.0
            
            try:
                gender = "Kadın"
                if driver.find_element(By.XPATH, "(//div[@class='jkj4C4LML4qv2Iq8GkL3']/div)[1]").text == "Cinsiyet":
                    gender = driver.find_element(By.XPATH, "(//div[@class='jkj4C4LML4qv2Iq8GkL3']/div)[2]").text
            except (NoSuchElementException, ValueError):
                gender = "Kadın"

            sizes = []

            try:
                size_elements = driver.find_elements(By.XPATH, "//span[@data-test-id='variant-box-name']")
                sizes = [size.text for size in size_elements]
            except (NoSuchElementException, ValueError):
                sizes = []

            try:
                color_element = driver.find_element(By.XPATH, "(//span[@data-test-id='variant-value'])[2]")
                color = color_element.text
            except (NoSuchElementException, ValueError):
                color = None            

            # Save product to the database
            category, _ = Category.objects.get_or_create(name="Günün Fırsatı")
            product, _ = Product.objects.update_or_create(
                name=title,
                defaults={
                    'brand': brand,
                    'product_link': link,
                    'rate': rate,
                    'consideration_num': consideration_num,
                    'seller': seller,
                    'description': f"Brand: {brand} - Rating: {rate} - Number of Reviews: {consideration_num} - Seller: {seller}",
                    'price': price,
                    'category': category,
                    'gender': gender,
                    'sizes': sizes,
                    'color': color
                }
            )

            # Save images to the product
            for image_url in images:
                if not product.images.filter(image_url=image_url).exists():
                    product.images.create(image_url=image_url)

        driver.quit()
        self.stdout.write(self.style.SUCCESS('Products successfully saved to the database'))