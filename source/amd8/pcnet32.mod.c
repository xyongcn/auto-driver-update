#include <linux/module.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

MODULE_INFO(vermagic, VERMAGIC_STRING);

__visible struct module __this_module
__attribute__((section(".gnu.linkonce.this_module"))) = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

static const struct modversion_info ____versions[]
__used
__attribute__((section("__versions"))) = {
	{ 0xbf8d6d33, __VMLINUX_SYMBOL_STR(module_layout) },
	{ 0x6f6eedb9, __VMLINUX_SYMBOL_STR(eth_change_mtu) },
	{ 0xe4759725, __VMLINUX_SYMBOL_STR(eth_validate_addr) },
	{ 0x96cf5261, __VMLINUX_SYMBOL_STR(eth_mac_addr) },
	{ 0x2f53601f, __VMLINUX_SYMBOL_STR(param_ops_int) },
	{ 0x8eb7f3b0, __VMLINUX_SYMBOL_STR(param_array_ops) },
	{ 0x340cd1df, __VMLINUX_SYMBOL_STR(pci_unregister_driver) },
	{ 0x437d7ebf, __VMLINUX_SYMBOL_STR(__pci_register_driver) },
	{ 0x2b652be8, __VMLINUX_SYMBOL_STR(consume_skb) },
	{ 0x8329e6f0, __VMLINUX_SYMBOL_STR(memset) },
	{ 0x636e7432, __VMLINUX_SYMBOL_STR(netif_device_attach) },
	{ 0xe1bd7dac, __VMLINUX_SYMBOL_STR(pci_restore_state) },
	{ 0x2072ee9b, __VMLINUX_SYMBOL_STR(request_threaded_irq) },
	{ 0x6005aa0b, __VMLINUX_SYMBOL_STR(__napi_complete) },
	{ 0x3a93fe26, __VMLINUX_SYMBOL_STR(netif_receive_skb_sk) },
	{ 0x8bb811fe, __VMLINUX_SYMBOL_STR(eth_type_trans) },
	{ 0xc3575ecc, __VMLINUX_SYMBOL_STR(skb_put) },
	{ 0x42188d7b, __VMLINUX_SYMBOL_STR(__netdev_alloc_skb) },
	{ 0x74a436c4, __VMLINUX_SYMBOL_STR(mem_section) },
	{ 0x56405134, __VMLINUX_SYMBOL_STR(pci_set_power_state) },
	{ 0x8d272b8b, __VMLINUX_SYMBOL_STR(pci_choose_state) },
	{ 0xc885070f, __VMLINUX_SYMBOL_STR(pci_save_state) },
	{ 0x2af153a9, __VMLINUX_SYMBOL_STR(netif_device_detach) },
	{ 0xf20dabd8, __VMLINUX_SYMBOL_STR(free_irq) },
	{ 0x706d051c, __VMLINUX_SYMBOL_STR(del_timer_sync) },
	{ 0x3ba6e97f, __VMLINUX_SYMBOL_STR(__dev_kfree_skb_any) },
	{ 0xe4016972, __VMLINUX_SYMBOL_STR(dma_ops) },
	{ 0xa4c6c875, __VMLINUX_SYMBOL_STR(netif_tx_wake_queue) },
	{ 0x1fedf0f4, __VMLINUX_SYMBOL_STR(__request_region) },
	{ 0x64384f8f, __VMLINUX_SYMBOL_STR(dma_supported) },
	{ 0x1f045c1d, __VMLINUX_SYMBOL_STR(pci_set_master) },
	{ 0x85d0f384, __VMLINUX_SYMBOL_STR(pci_enable_device) },
	{ 0xab600421, __VMLINUX_SYMBOL_STR(probe_irq_off) },
	{ 0xb121390a, __VMLINUX_SYMBOL_STR(probe_irq_on) },
	{ 0x83ba46ba, __VMLINUX_SYMBOL_STR(register_netdev) },
	{ 0x9580deb, __VMLINUX_SYMBOL_STR(init_timer_key) },
	{ 0x12da5bb2, __VMLINUX_SYMBOL_STR(__kmalloc) },
	{ 0x9645bf75, __VMLINUX_SYMBOL_STR(netif_napi_add) },
	{ 0x8d5bf968, __VMLINUX_SYMBOL_STR(dma_alloc_attrs) },
	{ 0x4a619f83, __VMLINUX_SYMBOL_STR(memcpy) },
	{ 0xb6e41883, __VMLINUX_SYMBOL_STR(memcmp) },
	{ 0xa8f2360f, __VMLINUX_SYMBOL_STR(alloc_etherdev_mqs) },
	{ 0x50eedeb8, __VMLINUX_SYMBOL_STR(printk) },
	{ 0xb81960ca, __VMLINUX_SYMBOL_STR(snprintf) },
	{ 0x73e20c1c, __VMLINUX_SYMBOL_STR(strlcpy) },
	{ 0x16e5c2a, __VMLINUX_SYMBOL_STR(mod_timer) },
	{ 0x91eb9b4, __VMLINUX_SYMBOL_STR(round_jiffies) },
	{ 0xda66ce9a, __VMLINUX_SYMBOL_STR(generic_mii_ioctl) },
	{ 0xfcec0987, __VMLINUX_SYMBOL_STR(enable_irq) },
	{ 0x3ce4ca6f, __VMLINUX_SYMBOL_STR(disable_irq) },
	{ 0x18090c51, __VMLINUX_SYMBOL_STR(mii_nway_restart) },
	{ 0x3c3fce39, __VMLINUX_SYMBOL_STR(__local_bh_enable_ip) },
	{ 0x7a2af7b4, __VMLINUX_SYMBOL_STR(cpu_number) },
	{ 0x4629334c, __VMLINUX_SYMBOL_STR(__preempt_count) },
	{ 0x51935f05, __VMLINUX_SYMBOL_STR(napi_disable) },
	{ 0x7d11c268, __VMLINUX_SYMBOL_STR(jiffies) },
	{ 0xeae3dfd6, __VMLINUX_SYMBOL_STR(__const_udelay) },
	{ 0xf9a482f9, __VMLINUX_SYMBOL_STR(msleep) },
	{ 0x26388f69, __VMLINUX_SYMBOL_STR(pci_disable_device) },
	{ 0xac246b57, __VMLINUX_SYMBOL_STR(free_netdev) },
	{ 0x7c61340c, __VMLINUX_SYMBOL_STR(__release_region) },
	{ 0xff7559e4, __VMLINUX_SYMBOL_STR(ioport_resource) },
	{ 0x15c965d6, __VMLINUX_SYMBOL_STR(unregister_netdev) },
	{ 0x8999751a, __VMLINUX_SYMBOL_STR(dma_free_attrs) },
	{ 0x37a0cba, __VMLINUX_SYMBOL_STR(kfree) },
	{ 0x92253b1d, __VMLINUX_SYMBOL_STR(mii_ethtool_sset) },
	{ 0x1916e38c, __VMLINUX_SYMBOL_STR(_raw_spin_unlock_irqrestore) },
	{ 0x680ec266, __VMLINUX_SYMBOL_STR(_raw_spin_lock_irqsave) },
	{ 0x87d4df01, __VMLINUX_SYMBOL_STR(mii_ethtool_gset) },
	{ 0xe690fde3, __VMLINUX_SYMBOL_STR(netdev_info) },
	{ 0xe44b6f34, __VMLINUX_SYMBOL_STR(netif_carrier_off) },
	{ 0xf409e834, __VMLINUX_SYMBOL_STR(netif_carrier_on) },
	{ 0x1951da63, __VMLINUX_SYMBOL_STR(mii_link_ok) },
	{ 0x6220b4a2, __VMLINUX_SYMBOL_STR(crc32_le) },
	{ 0xa7b63ea2, __VMLINUX_SYMBOL_STR(netdev_err) },
	{ 0x6bf1c17f, __VMLINUX_SYMBOL_STR(pv_lock_ops) },
	{ 0xf239e638, __VMLINUX_SYMBOL_STR(netdev_printk) },
	{ 0xbd19f2da, __VMLINUX_SYMBOL_STR(__napi_schedule) },
	{ 0xe259ae9e, __VMLINUX_SYMBOL_STR(_raw_spin_lock) },
	{ 0xb4390f9a, __VMLINUX_SYMBOL_STR(mcount) },
};

static const char __module_depends[]
__used
__attribute__((section(".modinfo"))) =
"depends=mii";

MODULE_ALIAS("pci:v00001022d00002001sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001022d00002000sv*sd*bc*sc*i*");
MODULE_ALIAS("pci:v00001023d00002000sv*sd*bc02sc00i*");

MODULE_INFO(srcversion, "4D7FF3A291B5D924F46D466");
