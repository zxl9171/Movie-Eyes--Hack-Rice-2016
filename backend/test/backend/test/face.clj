(ns backend.test.face
  (:require [clojure.test :refer :all]
            [backend.face :refer :all]))

(def data-example
  (array-map
    :u 10000
    :a 2011541224
    :k "AKID2ZkOXFyDRHZRlbPo93SMtzVY79kpAdGP"
    :e "1432970065"
    :t "1427786065"
    :r "270494647"
    :f ""))

(defn is= [a b]
  (is (= a b)))

(deftest test-signature
  (testing "sign"
    (is= "V1fNuvOMjHkX1Q4IudaPsd7Ks691PTEwMDAwJmE9MjAxMTU0MTIyNCZrPUFLSUQyWmtPWEZ5RFJIWlJsYlBvOTNTTXR6Vlk3OWtwQWRHUCZlPTE0MzI5NzAwNjUmdD0xNDI3Nzg2MDY1JnI9MjcwNDk0NjQ3JmY9"
      (with-redefs [secret-key "ckKU7P4FwB4PBZQlnB9hfBAcaKZMeUge"]
           (-> data-example dict-combine sign-message)))))
