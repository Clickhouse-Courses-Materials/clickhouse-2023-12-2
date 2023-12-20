terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
}

resource "yandex_vpc_network" "default_network" {
}

resource "yandex_vpc_subnet" "foo" {
  network_id     = yandex_vpc_network.default_network.id
  v4_cidr_blocks = ["10.5.0.0/24"]
  zone           = "ru-central1-a"
}

resource "yandex_mdb_clickhouse_cluster" "clickhouse_example" {
  environment             = "PRESTABLE"
  name                    = "clickhouse_example"
  network_id              = yandex_vpc_network.default_network.id
  sql_database_management = true
  sql_user_management     = true
  admin_password          = var.clickhouse_password
  version                 = "23.3"

  host {
    type             = "CLICKHOUSE"
    zone             = "ru-central1-a"
    subnet_id        = yandex_vpc_subnet.foo.id
    assign_public_ip = true
  }

  clickhouse {
    resources {
      resource_preset_id = "s3-c2-m8"
      disk_size          = 64
      disk_type_id       = "network-ssd"
    }

    config {
      log_level              = "TRACE"
      max_concurrent_queries = 100
      max_connections        = 100
    }
  }

  cloud_storage {
    enabled = false
  }

  maintenance_window {
    type = "ANYTIME"
  }
}