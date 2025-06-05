# from byprot.models.dplm import DiffusionProteinLanguageModel as DPLM
# from byprot.models.dplm2 import MultimodalDiffusionProteinLanguageModel as DPLM2
# from byprot.models.dplm2 import DPLM2Bit
# import os

# "Add HF_ENDPOINT=https://hf-mirror.com before python xxx"
# # os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# dplm = DPLM.from_pretrained("airkingbd/dplm_650m").cuda()
# dplm2 = DPLM2.from_pretrained("airkingbd/dplm2_650m").cuda()
# # dplm2_bit = DPLM2Bit.from_pretrained("airkingbd/dplm2_bit_650m").cuda()

# from generate_dplm import initialize_generation

# batch = initialize_generation(
#   length=200,
#   num_seqs=5,
#   tokenizer=dplm.tokenizer,
#   device=next(dplm.parameters()).device
# )
# print(batch)
# samples = dplm.generate(
#   batch=batch,
#   max_iter=10, #500
# )
# print(samples)
# # print(samples.shape)
# samples = samples[0]
# print([''.join(seq.split(' ')) for seq in dplm.tokenizer.batch_decode(samples, skip_special_tokens=True)])

from Bio.PDB import PDBParser
from Bio.PDB.PDBExceptions import PDBConstructionWarning
import warnings

# 抑制一些不重要的警告
warnings.simplefilter('ignore', PDBConstructionWarning)

def get_alpha_carbon_info(pdb_file):
    """
    读取PDB文件并返回每个氨基酸的α碳原子坐标和pLDDT值
    
    参数:
        pdb_file (str): PDB文件路径
        
    返回:
        list: 包含字典的列表，每个字典包含残基信息和CA原子数据
    """
    # 创建PDB解析器
    parser = PDBParser()
    
    # 解析PDB文件
    structure = parser.get_structure("protein", pdb_file)
    
    # 存储结果
    residues_info = []
    
    # 遍历所有模型、链和残基
    for model in structure:
        for chain in model:
            for residue in chain:
                # # 检查是否是氨基酸(排除水分子等)
                # if residue.get_resname().strip() not in PDBParser.PERMISSIVE_POLYPEPTIDE:
                #     continue
                
                # 尝试获取α碳原子
                try:
                    ca_atom = residue['CA']
                    res_info = {
                        'chain': chain.id,
                        'resname': residue.get_resname(),
                        'resnum': residue.id[1],
                        'ca_coord': ca_atom.get_coord().tolist(),
                        'plddt': ca_atom.get_bfactor()
                    }
                    residues_info.append(res_info)
                except KeyError:
                    # 如果该残基没有α碳原子
                    continue
                    
    return residues_info

# 使用示例
if __name__ == "__main__":
    pdb_file = "AF-Q9V168-F1-model_v4.pdb"  # 替换为你的PDB文件路径
    residues_data = get_alpha_carbon_info(pdb_file)
    
    # 打印结果
    print(f"Found {len(residues_data)} residues:")
    print("Chain ResName ResNum   CA X      CA Y      CA Z      pLDDT")
    print("---------------------------------------------------------")
    for res in residues_data:
        print(f"{res['chain']:4}  {res['resname']:5} {res['resnum']:5}  "
              f"{res['ca_coord'][0]:7.2f} {res['ca_coord'][1]:7.2f} {res['ca_coord'][2]:7.2f}  "
              f"{res['plddt']:5.1f}")
    
    # # 可选：保存为CSV文件
    # import csv
    # with open('ca_plddt_data.csv', 'w', newline='') as csvfile:
    #     fieldnames = ['chain', 'resname', 'resnum', 'ca_x', 'ca_y', 'ca_z', 'plddt']
    #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for res in residues_data:
    #         writer.writerow({
    #             'chain': res['chain'],
    #             'resname': res['resname'],
    #             'resnum': res['resnum'],
    #             'ca_x': res['ca_coord'][0],
    #             'ca_y': res['ca_coord'][1],
    #             'ca_z': res['ca_coord'][2],
    #             'plddt': res['plddt']
    #         })
    # print("\nData saved to 'ca_plddt_data.csv'")