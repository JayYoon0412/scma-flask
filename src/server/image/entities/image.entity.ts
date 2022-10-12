import {
  Column,
  CreateDateColumn,
  DeleteDateColumn,
  PrimaryGeneratedColumn,
} from 'typeorm';

@Object()
export class Image {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  src: string;

  @CreateDateColumn()
  uploadedAt: Date;

  @DeleteDateColumn()
  deletedAt: Date;
}
